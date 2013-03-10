# -*- coding: utf-8 -*-
from rest_framework.renderers import BrowsableAPIRenderer as BrowsableAPIRendererBase


class BrowsableAPIRenderer(BrowsableAPIRendererBase):

    def serializer_to_form_fields(self, serializer):

        fields  = super(BrowsableAPIRenderer, self).serializer_to_form_fields(serializer)
        initial = serializer.context.get('form_initial')

        if initial:

            for field_name, field in fields.items():

                if field_name in initial: field.initial = initial[field_name]

        return fields
