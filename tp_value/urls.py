# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from traceparent.utils import ordered_dict

from .views import UnitFilterView, UnitCreateView, UnitRetrieveView, \
    QuantityFilterView, QuantityRetrieveView, QuantityCreateView


class ValueView(APIView):

    def get(self, request):

        data = ordered_dict(
            {
             'unit': reverse('tp_value_unit', request=self.request),
             'quantity': reverse('tp_value_quantity', request=self.request),
            }
        )
        
        return Response(data)


class UnitView(APIView):

    def get(self, request):

        data = ordered_dict(
            {
             'create': reverse('tp_value_unit_create', request=self.request),
             'filter': reverse('tp_value_unit_filter', request=self.request),
            }
        )

        return Response(data)

        
class QuantityView(APIView):

    def get(self, request):

        data = ordered_dict(
            {
             'create': reverse('tp_value_quantity_create', request=self.request),
             'filter': reverse('tp_value_quantity_filter', request=self.request),
            }
        )

        return Response(data)


urlpatterns = patterns('',

    # Root
    url(r'^$', ValueView.as_view(), name='tp_value'),

    # Unit
    url(r'^unit/$', UnitView.as_view(), name='tp_value_unit'),
    url(r'^unit/filter/$', UnitFilterView.as_view(), name='tp_value_unit_filter'),
    url(r'^unit/create/$', UnitCreateView.as_view(), name='tp_value_unit_create'),
    url(r'^unit/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/$',
        UnitRetrieveView.as_view(), name='tp_value_unit_retrieve'),

    # Quantity
    url(r'^quantity/$', QuantityView.as_view(), name='tp_value_quantity'),
    url(r'^quantity/filter/$', QuantityFilterView.as_view(), name='tp_value_quantity_filter'),
    url(r'^quantity/create/$', QuantityCreateView.as_view(), name='tp_value_quantity_create'),
    url(r'^quantity/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/$',
        QuantityRetrieveView.as_view(), name='tp_value_quantity_retrieve'),
)
