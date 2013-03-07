# -*- coding: utf-8 -*-
import decimal

from django.db import models
from tp_auth.models import User

from django_extensions.db.fields import UUIDField

from traceparent import settings


class Unit(models.Model):

    uuid           = UUIDField(auto=True, primary_key=True)
    creator        = models.ForeignKey(User)
    name           = models.CharField(max_length=128)
    slug           = models.SlugField(max_length=128)
    symbol         = models.CharField(max_length=8)
    decimal_places = models.PositiveIntegerField(default=2, null=True, blank=True)
    #datetime       = models.DateTimeField(auto_now_add=True)

    def __unicode__(self): return u'%s (%s)' % (self.name, self.symbol)

value_status_choices = (
                        ('symbolic',  u'symbolic'),
                        ('pending',   u'pending'),
                        ('present',   u'present'),
                        ('passed',    u'passed'),
                        ('rejected',  u'rejected'),
                        ('cancelled', u'cancelled'),
                       )

class Quantity(models.Model):

    uuid     = UUIDField(auto=True, primary_key=True)
    creator  = models.ForeignKey(User, null=True, blank=True,
                                 related_name="quantities_created")
    unit     = models.ForeignKey(Unit)
    quantity = models.DecimalField(**settings.TP_VALUE_QUANTITY_DECIMAL_MODEL_ATTRS)
    user     = models.ForeignKey(User, null=True, blank=True, related_name='quantities')
    #creation_datetime = models.DateTimeField(auto_now_add=True)
    datetime = models.DateTimeField(auto_now_add=True)
    prev     = models.ManyToManyField('self', null=True, blank=True,
                                      symmetrical=False, related_name='next')
    status   = models.SlugField(default='symbolic', max_length=64,
                                     choices=value_status_choices)
#    balanced      = models.BooleanField()

    def __unicode__(self):
        
        return u'%s%s %s' % (self.quantity.quantize(decimal.Decimal(10) ** \
                             -self.unit.decimal_places),
                             self.unit.symbol, self.user)

    def save(self, *args, **kwargs):

        # Needs an primary key prior to saving the 'ManyToManyField' field.
        if not self.uuid: self.uuid = self._meta.get_field("uuid").create_uuid()

        super(Quantity, self).save(*args, **kwargs)

    class Meta:

        verbose_name_plural = "Quantities"
        ordering            = ['-datetime']
