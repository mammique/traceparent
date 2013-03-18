# -*- coding: utf-8 -*-
import decimal

from django.db import models

from django_extensions.db.fields import UUIDField

from traceparent import settings
from traceparent.fields import SlugBlankToNoneField

from tp_auth.models import User


class Unit(models.Model):

    uuid           = UUIDField(auto=True, primary_key=True)
    creator        = models.ForeignKey(User)
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
                       ]


class Quantity(models.Model):

    uuid              = UUIDField(auto=True, primary_key=True)
    creator           = models.ForeignKey(User, # null=True, blank=True,
                            related_name="quantities_created")
    user              = models.ForeignKey(User, # null=True, blank=True,
                            related_name='quantities')
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

    def save(self, *args, **kwargs):

        # Needs an primary key prior to saving the 'ManyToManyField' field.
        if not self.uuid: self.uuid = self._meta.get_field("uuid").create_uuid()

        super(Quantity, self).save(*args, **kwargs)
