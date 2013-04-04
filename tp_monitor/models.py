# -*- coding: utf-8 -*-
import decimal

from django.db import models

from traceparent import settings
from traceparent.fields import SlugBlankToNoneField, DecimalBlankToNoneField
from traceparent.models import UUIDModel

from tp_auth.models import User
from tp_value.models import Unit, QuantityStatus, Quantity, quantity__unicode__


class Scope(UUIDModel):

    creator    = models.ForeignKey(User, related_name='scopes_created')
    user       = models.ForeignKey(User, related_name='scopes')
    quantities = models.ManyToManyField(Quantity, null=True, blank=True,
                     related_name='scopes')
    datetime   = models.DateTimeField(auto_now_add=True)

    class Meta:

        ordering = ['-datetime']

    def __unicode__(self):
        return u'<%s> %s' % (self.pk, self.user)


class Counter(UUIDModel):

    creator        = models.ForeignKey(User, related_name='counters_created')
    user           = models.ForeignKey(User, related_name='counters')
    datetime       = models.DateTimeField(auto_now_add=True)
    datetime_start = models.DateTimeField(null=True, blank=True, default=None)
    datetime_stop  = models.DateTimeField(null=True, blank=True, default=None)
    scopes         = models.ManyToManyField(Scope, related_name='counters')
    quantities     = models.ManyToManyField(Quantity, null=True, blank=True,
                         related_name='counters')
    class Meta:

        ordering = ['-datetime']

    def __unicode__(self):
        return u'(%s > %s) <%s> %s' % \
                   (self.datetime_start, self.datetime_stop, self.pk, self.user)


#class QuantityResult(UUIDModel):
#
    #quantity    = models.DecimalField(**settings.TP_VALUE_QUANTITY_DECIMAL_MODEL_ATTRS)
    #unit        = models.ForeignKey(Unit)
    #status      = models.ForeignKey(QuantityStatus)
    #datetime    = models.DateTimeField(auto_now=True)
#
    #class Meta:
#
        #ordering = ['-datetime']
#
    #def __unicode__(self): return quantity__unicode__(self)


class ResultSum(UUIDModel):

    quantity  = models.DecimalField(**settings.TP_VALUE_QUANTITY_DECIMAL_MODEL_ATTRS)
    unit      = models.ForeignKey(Unit)
    status    = models.ForeignKey(QuantityStatus)
    datetime  = models.DateTimeField(auto_now=True)
    counter   = models.ForeignKey(Counter, related_name='sums')

    class Meta:

        ordering = ['-datetime']

    #def __unicode__(self): return quantity__unicode__(self)


class Mark(UUIDModel):

    quantity = DecimalBlankToNoneField(null=True, blank=True, **settings.TP_VALUE_QUANTITY_DECIMAL_MODEL_ATTRS)
    unit     = models.ForeignKey(Unit)
    statuses = models.ManyToManyField(QuantityStatus, related_name='marks')
    creator  = models.ForeignKey(User, related_name='marks_created')
    user     = models.ForeignKey(User, related_name='marks')
    datetime = models.DateTimeField(auto_now_add=True)
    counters = models.ManyToManyField(Counter, related_name='marks')

    class Meta:

        ordering = ['-datetime']

#    def __unicode__(self): return quantity__unicode__(self)


def counter_update(counter):

    filter_kwargs      = []
    filter_kwargs_dict = {}

    for v in counter.marks.all().values('unit', 'statuses'):

        v['status'] = v.pop('statuses')

        if not v['unit'] in filter_kwargs_dict: filter_kwargs_dict[v['unit']] = []

        if not v['status'] in filter_kwargs_dict[v['unit']]:

            filter_kwargs_dict[v['unit']].append(v['status'])
            filter_kwargs.append(v)

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

    for f in filter_kwargs:

        f_get = {'unit': Unit.objects.get(pk=f['unit']),
                 'status': QuantityStatus.objects.get(pk=f['status'])}

        try: s = counter.sums.get(**f_get)

        # FIXME: use get_or_create()?
        except ResultSum.DoesNotExist:

            f_get['counter'] = counter
            s = ResultSum(**f_get)
        
        q = counter.quantities.filter(**f).aggregate(models.Sum('quantity'))['quantity__sum']

        if q == None: continue

        s.quantity = q
        s.save()
        filter_kwargs_new.append(f)

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


# Newly created `Mark` cannot list its counters until m2m_changed is called.
def monitor_m2m_changed(instance=None, *args, **kwargs):

    if not instance: return

    # Mark
    if isinstance(instance, Mark) and kwargs.get('action', None) == 'post_add':

        map(lambda c: counter_update(c), instance.counters.all())
        return

models.signals.m2m_changed.connect(monitor_m2m_changed)
