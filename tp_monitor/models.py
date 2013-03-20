# -*- coding: utf-8 -*-
# import decimal

from django.db import models

from django_extensions.db.fields import UUIDField

from traceparent import settings

from tp_auth.models import User
from tp_value.models import Unit, Quantity


#class Countity(models.Model):

#    uuid            = UUIDField(auto=True, primary_key=True)
#    creator         = models.ForeignKey(User, related_name='countities_created')
#    user            = models.ForeignKey(User, related_name='countities')
#    quantity        = models.DecimalField(**settings.TP_VALUE_QUANTITY_DECIMAL_MODEL_ATTRS)
#    unit            = models.ForeignKey(Unit)
#    datetime        = models.DateTimeField(auto_now_add=True)
#    datetime_update = models.DateTimeField(auto_now=True)


class Counter(models.Model):

    uuid           = UUIDField(auto=True, primary_key=True)
    creator        = models.ForeignKey(User, related_name='counters_created')
    user           = models.ForeignKey(User, related_name='counters')
    quantities     = models.ManyToManyField(Quantity, null=True,
                         related_name='counters')
    datetime       = models.DateTimeField(auto_now_add=True)
    datetime_start = models.DateTimeField(null=True, blank=True, default=None)
    datetime_stop  = models.DateTimeField(null=True, blank=True, default=None)

    ## Countities
    #sums           = models.ManyToManyField(Countity, null=True,
    #                                        related_name='counter_sums')
    #graduations    = models.ManyToManyField(Countity, null=True,
    #                                        related_name='counter_graduations')

    class Meta:

        ordering = ['-datetime']

    def __unicode__(self):
        return u'(%s-%s) <%s> %s' % \
                   (self.datetime_start, self.datetime_stop, self.pk, self.user)


#class Countity(object):

#    uuid     = UUIDField(auto=True, primary_key=True)
#    quantity = models.DecimalField(**settings.TP_VALUE_QUANTITY_DECIMAL_MODEL_ATTRS)
#    unit     = models.ForeignKey(Unit)
#    datetime = models.DateTimeField(auto_now_add=True)


#class QuantityResult(Countity, models.Model):

#    datetime_update = models.DateTimeField(auto_now=True)
#    counter_sum     = models.ForeignKey(User, related_name='sums')


#class Graduation(Countity, models.Model):

#    creator  = models.ForeignKey(User, related_name='countities_created')
#    user     = models.ForeignKey(User, related_name='countities')
#    counters = models.ManyToManyField(Counter, null=True, related_name='graduations')
