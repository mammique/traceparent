# -*- coding: utf-8 -*-
import decimal

from django.db import models

from traceparent import settings
from traceparent.fields import SlugBlankToNoneField
from traceparent.models import UUIDModel

from tp_auth.models import User
from tp_value.models import Unit, Quantity, value_status_choices


#class Countity(models.Model):

#    uuid            = UUIDField(auto=True, primary_key=True)
#    creator         = models.ForeignKey(User, related_name='countities_created')
#    user            = models.ForeignKey(User, related_name='countities')
#    quantity        = models.DecimalField(**settings.TP_VALUE_QUANTITY_DECIMAL_MODEL_ATTRS)
#    unit            = models.ForeignKey(Unit)
#    datetime        = models.DateTimeField(auto_now_add=True)
#    datetime_update = models.DateTimeField(auto_now=True)


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

    #@property
    #def quantities(self):

    #    kwargs = {}

    #    # TODO: change 'datetime' to 'datetime_created' after migration.
    #    if self.datetime_start: kwargs['datetime__gte'] = self.datetime_start
    #    if self.datetime_stop:  kwargs['datetime__lte'] = self.datetime_stop

    #    return Quantity.objects.filter(scopes__in=self.scopes.all(), **kwargs)

    class Meta:

        ordering = ['-datetime']

    def __unicode__(self):
        return u'(%s > %s) <%s> %s' % \
                   (self.datetime_start, self.datetime_stop, self.pk, self.user)


class QuantityResult(UUIDModel):

    quantity    = models.DecimalField(**settings.TP_VALUE_QUANTITY_DECIMAL_MODEL_ATTRS)
    unit        = models.ForeignKey(Unit)
    status      = SlugBlankToNoneField(null=True, blank=True, default=None,
                      max_length=64, choices=value_status_choices)
    datetime    = models.DateTimeField(auto_now=True)
    counter_sum = models.ForeignKey(User, related_name='sums')

    #def __unicode__(self): return Quantity.__unicode__(self)


class Mark(UUIDModel):

    quantity = models.DecimalField(**settings.TP_VALUE_QUANTITY_DECIMAL_MODEL_ATTRS)
    unit     = models.ForeignKey(Unit)
    status   = SlugBlankToNoneField(null=True, blank=True, default=None,
                   max_length=64, choices=value_status_choices)
    creator  = models.ForeignKey(User, related_name='countities_created')
    user     = models.ForeignKey(User, related_name='countities')
    datetime = models.DateTimeField(auto_now_add=True)
    counters = models.ManyToManyField(Counter, related_name='marks')

    #def __unicode__(self): return Quantity.__unicode__(self)
