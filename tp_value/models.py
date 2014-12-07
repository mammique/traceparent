# -*- coding: utf-8 -*-
import decimal

from django.db import models

from traceparent import settings
from traceparent.fields import SlugBlankToNoneField
from traceparent.models import UUIDModel
from traceparent.utils import blanks_prune

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
        return u'%s %s' % \
            (self.__unicode__short__(), self.creator) # FIXME: creator/user

    def __unicode__short__(self):
        return u'%s (%s) <%s>' % \
            (self.name, self.symbol, self.pk) # FIXME: creator/user


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


class ConverterScriptError(Exception):

    def __init__(self, detail): self.detail = detail

    def __str__(self): return repr(self.detail)


class Converter(UUIDModel):

    creator  = models.ForeignKey(User, # null=True, blank=True,
                   related_name="converters_created")
    user     = models.ForeignKey(User, db_index=True, # null=True, blank=True,
                   related_name='converters')
    unit_in  = models.ForeignKey(Unit, related_name='converters_in')
    unit_out = models.ForeignKey(Unit, related_name='converters_out')
    #slug     = models.SlugField(db_index=True, max_length=128)
    type     = models.SlugField(db_index=True, max_length=64,
                   choices=(('operation_basic', 'operation_basic',),), default='operation_basic')
                   # IMPLEMENTME: stack_basic_1_row http://fsharpforfunandprofit.com/posts/stack-based-calculator/
    script   = models.TextField()

    def __init__(self, *args, **kwargs):

        r = super(Converter, self).__init__(*args, **kwargs)

        if self.script: self._script_load()

        return r

    def save(self, *args, **kwargs):

        if self.script: self._script_load()

        return super(Converter, self).save(*args, **kwargs)

    def _script_load(self):

        script, script_type, extra = self._script_parse(self.script, self.type)

        if script_type == 'operation_basic': self._script_eval = extra
        else: raise ConverterScriptError('Invalid type.')

    def _script_parse(self, script, script_type):

        extra = None

        if script_type == 'operation_basic':

            script       = blanks_prune(script).split(' ')
            script_clean = []
            operands     = ['+', '-', '*', '/']
            script_eval  = []

            for x in script:

                if not x in operands + ['quantity_in']:

                    try: x = '%s' % decimal.Decimal(x)
                    except decimal.InvalidOperation: raise ConverterScriptError('"%s" is not a valid number.' % x)

                script_clean.append(x)

                if x in operands: script_eval.append(x)
                else: script_eval.append('decimal.Decimal("%s")' % x)

            script = ' '.join(script_clean)
            extra  = ' '.join(script_eval)

        else: raise ConverterScriptError('Invalid type.')

        self.convert(decimal.Decimal(0), script_eval, script_type, extra)

        return script, script_type, extra

    def convert(self, q, s=None, s_type=None, extra=None):

        if not isinstance(q, decimal.Decimal): raise ConverterScriptError('"%s" is not a Decimal.' % q) # raise TypeError

        script = s or self.script

        if s != None: script_type = s_type
        else: script_type = self.type

        if not script: raise ConverterScriptError('No script specified.')

        if script_type == 'operation_basic':

            if s != None: evaluable = extra
            else: evaluable = getattr(self, '_script_eval', None)

            if not evaluable: raise ConverterScriptError('Evaluable script missing.')

            try: return eval(evaluable.replace('quantity_in', '%s' % q))
            except: raise ConverterScriptError('Script error.')

        else: raise ConverterScriptError('Invalid type.')

    def __unicode__(self):

        return u'%s <%s>' % \
                   (self.__unicode__short__(), self.pk,)

    def __unicode__short__(self):

        return u'%s > %s' % \
                   (self.unit_in.__unicode__short__(), self.unit_out.__unicode__short__(),)
