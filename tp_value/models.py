# -*- coding: utf-8 -*-
import decimal

from django.db import models

from traceparent import settings
from traceparent.fields import SlugBlankToNoneField
from traceparent.models import UUIDModel

from tp_auth.models import User
from tp_auth import VISIBILITY_CHOICES


class Unit(UUIDModel):

    creator        = models.ForeignKey(User, related_name='units_created')
    # FIXME: user
    name           = models.CharField(max_length=128)
    slug           = models.SlugField(max_length=128)
    symbol         = models.CharField(max_length=8)
    decimal_places = models.PositiveIntegerField(default=2) # FIXME: non-null.
    #datetime       = models.DateTimeField(auto_now_add=True)

    class Meta:

        ordering = ['-name',] # '-datetime']

    def __unicode__(self):
        return u'%s (%s) <%s> %s' % \
            (self.name, self.symbol, self.pk, self.creator) # FIXME: creator/user


value_status_choices = models.fields.BLANK_CHOICE_DASH + [
                        ('pending',   u'pending'),
                        ('present',   u'present'),
                        ('passed',    u'passed'),
                        ('rejected',  u'rejected'),
                        ('cancelled', u'cancelled'),
                        # ('locked',    u'locked'),
                        # ('frozen',    u'frozen'),
                       ]


class Quantity(UUIDModel):

    creator           = models.ForeignKey(User, # null=True, blank=True,
                            related_name="quantities_created")
    user              = models.ForeignKey(User, # null=True, blank=True,
                            related_name='quantities')
    user_visibility   = models.SlugField(default='public', max_length=64,
                            choices=VISIBILITY_CHOICES)
    unit              = models.ForeignKey(Unit)
    quantity          = models.DecimalField(**settings.TP_VALUE_QUANTITY_DECIMAL_MODEL_ATTRS)
    #creation_datetime = models.DateTimeField(auto_now_add=True)
    datetime          = models.DateTimeField(auto_now_add=True)
    prev              = models.ManyToManyField('self', null=True,
                            symmetrical=False, related_name='next')
    status            = SlugBlankToNoneField(null=True, blank=True, default=None,
                            max_length=64, choices=value_status_choices)

    class Meta:

        verbose_name_plural = "Quantities"
        ordering            = ['-datetime']

    def __unicode__(self):

        pk = "<%s>" if self.status != None else "*%s*"
        pk = pk % self.pk

        return u'%s%s %s %s' % (self.quantity.quantize(decimal.Decimal(10) ** \
                             -self.unit.decimal_places),
                             self.unit.symbol, pk, self.user)
