# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe

from rest_framework.renderers import BrowsableAPIRenderer as BrowsableAPIRendererBase


class BrowsableAPIRenderer(BrowsableAPIRendererBase):

    def get_description(self, *args, **kwargs):

        desc = super(BrowsableAPIRenderer, self).get_description(*args, **kwargs)
        return mark_safe('<div class="description prettyprint">%s</div>' % desc)

    def serializer_to_form_fields(self, serializer):

        fields  = super(BrowsableAPIRenderer, self).serializer_to_form_fields(serializer)
        initial = serializer.context.get('form_initial')

        if initial:

            for field_name, field in fields.items():

                if field_name in initial: field.initial = initial[field_name]

        return fields


class FormRenderer(BrowsableAPIRendererBase):

    media_type = 'text/html'
    format = 'form'
    template = 'rest_framework/api_form.html'


    ## https://github.com/tomchristie/django-rest-framework/blob/3357a36e37f83c04d161662def9cc5221761986c/rest_framework/renderers.py#L374
    #def get_form(self, view, method, request):
    #    from django import forms
    #    from rest_framework import parsers
    #    obj = getattr(view, 'object', None)
    #    if not self.show_form_for_method(view, method, request, obj):
    #        return

    #    if method in ('DELETE', 'OPTIONS'):
    #        return True  # Don't actually need to return a form

    #    if not getattr(view, 'get_serializer', None) or not parsers.FormParser in view.parser_classes:
    #        return

    #    serializer = view.get_serializer(instance=obj, method=method)
    #    fields = self.serializer_to_form_fields(serializer)

    #    # Creating an on the fly form see:
    #    # http://stackoverflow.com/questions/3915024/dynamically-creating-classes-python
    #    OnTheFlyForm = type(str("OnTheFlyForm"), (forms.Form,), fields)
    #    data = (obj is not None) and serializer.data or None
    #    form_instance = OnTheFlyForm(data)
    #    return form_instance
