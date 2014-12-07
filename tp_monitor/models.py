# -*- coding: utf-8 -*-
import decimal

from django.db import models

from traceparent import settings
from traceparent.fields import SlugBlankToNoneField, DecimalBlankToNoneField
from traceparent.models import UUIDModel

from tp_auth.models import User
from tp_value.models import Unit, QuantityStatus, Quantity, Converter, quantity__unicode__


class Scope(UUIDModel):

    creator    = models.ForeignKey(User, related_name='scopes_created')
    user       = models.ForeignKey(User, db_index=True, related_name='scopes')
    quantities = models.ManyToManyField(Quantity, db_index=True, null=True, blank=True,
                     related_name='scopes')
    datetime   = models.DateTimeField(db_index=True, auto_now_add=True)

    class Meta:

        ordering = ['-datetime']

    def __unicode__(self):
        return u'<%s> %s' % (self.pk, self.user)


class Counter(UUIDModel):

    creator        = models.ForeignKey(User, related_name='counters_created')
    user           = models.ForeignKey(User, db_index=True, related_name='counters')
    datetime       = models.DateTimeField(db_index=True, auto_now_add=True)
    datetime_start = models.DateTimeField(db_index=True, null=True, blank=True, default=None)
    datetime_stop  = models.DateTimeField(db_index=True, null=True, blank=True, default=None)
    scopes         = models.ManyToManyField(Scope, db_index=True, related_name='counters')
    quantities     = models.ManyToManyField(Quantity, db_index=True, null=True, blank=True,
                         related_name='counters')
    converters     = models.ManyToManyField(Converter, db_index=True, null=True, blank=True,
                         related_name='counters')

    class Meta:

        ordering = ['-datetime']

    def __unicode__(self):
        return u'(%s > %s) <%s> %s' % \
                   (self.datetime_start, self.datetime_stop, self.pk, self.user)


class Result(UUIDModel):

    quantity  = models.DecimalField(**settings.TP_VALUE_QUANTITY_DECIMAL_MODEL_ATTRS)
    unit      = models.ForeignKey(Unit)
    status    = models.ForeignKey(QuantityStatus)
    datetime  = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True
        ordering = ['-datetime']

    #def __unicode__(self): return quantity__unicode__(self)


class ResultSum(Result):

    counter = models.ForeignKey(Counter, related_name='sums')
    mode    = models.SlugField(db_index=True, max_length=64,
                 choices=(('normal',    'normal'),
                          ('converted', 'converted'),
                          ('combined',  'combined'),), default='normal')


class Mark(UUIDModel):

    quantity = DecimalBlankToNoneField(null=True, blank=True, db_index=True, **settings.TP_VALUE_QUANTITY_DECIMAL_MODEL_ATTRS)
    unit     = models.ForeignKey(Unit, db_index=True)
    statuses = models.ManyToManyField(QuantityStatus, db_index=True, related_name='marks')
    creator  = models.ForeignKey(User, related_name='marks_created')
    user     = models.ForeignKey(User, db_index=True, related_name='marks')
    datetime = models.DateTimeField(db_index=True, auto_now_add=True)
    counters = models.ManyToManyField(Counter, db_index=True, related_name='marks')

    class Meta:

        ordering = ['-datetime']

#    def __unicode__(self): return quantity__unicode__(self)


def counter_update(counter):

    filter_kwargs            = []
    filter_kwargs_dict       = {}
    filter_kwargs_normal_sum = []

    # Select `Unit`s and their `QuantityStatus`s from defined `Mark`s.
    for v in counter.marks.all().values('unit', 'statuses'):

        v['status'] = v.pop('statuses')

        if not v['unit'] in filter_kwargs_dict: filter_kwargs_dict[v['unit']] = []

        if not v['status'] in filter_kwargs_dict[v['unit']]:
            filter_kwargs_dict[v['unit']].append(v['status'])

    for unit, statuses in filter_kwargs_dict.items():
        for status in statuses: filter_kwargs_normal_sum.append({'unit': unit, 'status': status})

    # Select `Unit`s and their `QuantityStatus`s from convertable `Unit`s.
    for unit, statuses in filter_kwargs_dict.items():

        for converter in counter.converters.filter(unit_out=unit):

            if not converter.unit_in.pk in filter_kwargs_dict:

                filter_kwargs_dict[converter.unit_in.pk] = statuses

            else:

                filter_kwargs_dict[converter.unit_in.pk] = \
                    list(set(filter_kwargs_dict[converter.unit_in.pk] + statuses))

    for unit, statuses in filter_kwargs_dict.items():
        for status in statuses: filter_kwargs.append({'unit': unit, 'status': status})

    queryset = Quantity.objects.none()

    for s in counter.scopes.all():

        date_range = {}
        if counter.datetime_start: date_range['datetime__gte'] = counter.datetime_start
        if counter.datetime_stop:  date_range['datetime__lte'] = counter.datetime_stop
        if date_range: quantities = s.quantities.filter(**date_range)
        else: quantities = s.quantities.all()

        for f in filter_kwargs: queryset = queryset | quantities.filter(models.Q(**f))

    counter.quantities = queryset.distinct()

    filter_kwargs_new = []

    for f in filter_kwargs_normal_sum:

        unit = Unit.objects.get(pk=f['unit'])

        # Normal sum.
        f_get = {'unit':   unit,
                 'status': QuantityStatus.objects.get(pk=f['status']),
                 'mode':   'normal'}

        q      = counter.quantities.filter(**f).aggregate(models.Sum('quantity'))['quantity__sum']
        q_conv = None

        for converter in counter.converters.filter(unit_out=unit):

            f_conv = f.copy()
            f_conv['unit'] = converter.unit_in

            q_in = counter.quantities.filter(**f_conv).aggregate(models.Sum('quantity'))['quantity__sum']

            if q_in != None:

                q_out = converter.convert(q_in)

                if q_conv == None: q_conv = decimal.Decimal(0)

                q_conv += q_out

        # Sum.
        if q != None:

            try: s = counter.sums.get(**f_get)

            except ResultSum.DoesNotExist:

                s = ResultSum(**f_get)
                s.counter = counter

            s.quantity = q
            s.save()
            filter_kwargs_new.append(f_get)

        # Converted sum.
        if q_conv != None:

            f_conv_get = f_get.copy()
            f_conv_get['mode'] = 'converted'

            try: s_conv = counter.sums.get(**f_conv_get)

            except ResultSum.DoesNotExist:

                s_conv = ResultSum(**f_conv_get)
                s_conv.counter = counter

            s_conv.quantity = q_conv
            s_conv.save()
            filter_kwargs_new.append(f_conv_get)

            # Combined sum.
            f_comb_get = f_get.copy()
            f_comb_get['mode'] = 'combined'

            try: s_comb = counter.sums.get(**f_comb_get)

            except ResultSum.DoesNotExist:

                s_comb = ResultSum(**f_comb_get)
                s_comb.counter = counter

            s_comb.quantity = q_conv
            if q != None: s_comb.quantity += q

            s_comb.save()
            filter_kwargs_new.append(f_comb_get)

    queryset = counter.sums.all()
    for f in filter_kwargs_new: queryset = queryset.exclude(models.Q(**f))
    queryset.all().delete()


def monitor_post_save(instance=None, *args, **kwargs):

    if not instance: return

    # Quantity
    if isinstance(instance, Quantity):

        map(lambda c: counter_update(c),
            Counter.objects.filter(scopes__in=instance.scopes.all()))
        return

    # Converter
    if isinstance(instance, Converter):

        map(lambda c: counter_update(c), instance.counters.all())
        return

    # Scope
    if isinstance(instance, Scope):

        map(lambda c: counter_update(c), instance.counters.all())
        return

    # Counter
    if isinstance(instance, Counter):

        counter_update(instance)
        return

    # Mark
    if isinstance(instance, Mark):

        map(lambda c: counter_update(c), instance.counters.all())
        return

models.signals.post_save.connect(monitor_post_save)


def monitor_m2m_changed(instance=None, *args, **kwargs):

    # Newly created `Mark` cannot list its counters until this signal.
    if isinstance(instance, Mark) and kwargs.get('action', None) == 'post_add':

        map(lambda c: counter_update(c), instance.counters.all())
        return

    # `Converter`s added or deleted from a `Counter` cannot be listed until this signal.
    if isinstance(instance, Counter) and kwargs.get('action', None) in ('post_add', 'post_clear',) and \
        issubclass(kwargs.get('model', None), Converter): counter_update(instance)

models.signals.m2m_changed.connect(monitor_m2m_changed)
