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
    name           = models.CharField(db_index=True, max_length=128)
    slug           = models.SlugField(db_index=True, max_length=128)
    symbol         = models.CharField(db_index=True, max_length=8)
    decimal_places = models.PositiveIntegerField(default=2) # FIXME: non-null.
    #datetime       = models.DateTimeField(auto_now_add=True)

    class Meta:

        ordering = ['name',] # '-datetime']

    def __unicode__(self):
        return u'%s (%s) <%s> %s' % \
            (self.name, self.symbol, self.pk, self.creator) # FIXME: creator/user


class QuantityStatus(models.Model):
	
    slug = models.SlugField(primary_key=True, db_index=True, max_length=64)

    class Meta:

        verbose_name_plural = "quantity statuses"
        ordering            = ['-slug']

    def __unicode__(self): return self.slug


class Quantity(UUIDModel):

    creator           = models.ForeignKey(User, # null=True, blank=True,
                            related_name="quantities_created")
    user              = models.ForeignKey(User, db_index=True, # null=True, blank=True,
                            related_name='quantities')
    user_visibility   = models.SlugField(default='public', max_length=64,
                            choices=VISIBILITY_CHOICES)
    unit              = models.ForeignKey(Unit, db_index=True)
    quantity          = models.DecimalField(db_index=True, **settings.TP_VALUE_QUANTITY_DECIMAL_MODEL_ATTRS)
    #creation_datetime = models.DateTimeField(auto_now_add=True)
    #datetime_legal   = models.DateTimeField()
    datetime          = models.DateTimeField(db_index=True, auto_now_add=True)
    prev              = models.ManyToManyField('self', null=True,
                            db_index=True, symmetrical=False, related_name='next')
    status            = models.ForeignKey(QuantityStatus, db_index=True, related_name='quantities')

    class Meta:

        verbose_name_plural = "quantities"
        ordering            = ['-datetime']

    def __unicode__(self): return quantity__unicode__(self)


def quantity__unicode__(q):

    pk = "<%s>" if q.status.slug != 'symbolic' else "*%s*"
    pk = pk % q.pk

    return u'%s%s %s %s' % (q.quantity.quantize(decimal.Decimal(10) ** \
                                -q.unit.decimal_places), q.unit.symbol, pk, q.user)
