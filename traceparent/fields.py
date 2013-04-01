# -*- coding: utf-8 -*-
from django.http import QueryDict
from django.db import models

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^traceparent\.fields\.SlugBlankToNoneField"])

from rest_framework import serializers
from rest_framework.reverse import reverse


class HyperlinkedFilterField(serializers.Field):

    def __init__(self, *args, **kwargs):

        self.view_name          = kwargs.pop('view_name')
        self.format             = kwargs.pop('format', None)
        self.lookup_params      = kwargs.pop('lookup_params')
        self.lookup_test        = kwargs.pop('lookup_test', None)
        self.querystring_params = kwargs.pop('querystring_params', {})

        return super(HyperlinkedFilterField, self).__init__(*args, **kwargs)

    def field_to_native(self, o, *args, **kwargs):

        if self.lookup_test and not self.lookup_test(o): return None

        view_name = self.view_name
        request   = self.context.get('request', None)
        format    = self.format or self.context.get('format', None)

        query = QueryDict('', mutable=True)
        for key, field in self.lookup_params.items():
            query[key] = getattr(o, field)

        query.update(self.querystring_params)

        return '%s?%s' % (reverse(view_name, request=request, format=format),
                    query.urlencode())



class BlankToNoneField(object):

    def to_python(self, value):

        if value == '': value = None

        return super(BlankToNoneField, self).to_python(value)


class SlugBlankToNoneField(BlankToNoneField, models.SlugField): pass
class DecimalBlankToNoneField(BlankToNoneField, models.DecimalField): pass
