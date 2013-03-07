# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .views import UnitFilterView, UnitCreateView, QuantityFilterView, QuantityCreateView


class ValueView(APIView):

    def get(self, request):

        return Response(
                        {
                         'unit': reverse('tp_value_unit', request=self.request),
                         'quantity': reverse('tp_value_quantity', request=self.request),
                        }
                       )

class UnitView(APIView):

    def get(self, request):

        return Response(
                        {
                         'create': reverse('tp_value_unit_create', request=self.request),
                         'filter': reverse('tp_value_unit_filter', request=self.request),
                        }
                       )

        
class QuantityView(APIView):

    def get(self, request):

        return Response(
                        {
                         'create': reverse('tp_value_quantity_create', request=self.request),
                         'filter': reverse('tp_value_quantity_filter', request=self.request),
                        }
                       )


urlpatterns = patterns('',

    # Root
    url(r'^$', ValueView.as_view(), name='tp_value'),

    # Unit
    url(r'^unit/$', UnitView.as_view(), name='tp_value_unit'),
    url(r'^unit/filter/$', UnitFilterView.as_view(), name='tp_value_unit_filter'),
    url(r'^unit/create/$', UnitCreateView.as_view(), name='tp_value_unit_create'),

    # Quantity
    url(r'^quantity/$', QuantityView.as_view(), name='tp_value_quantity'),
    url(r'^quantity/filter/$', QuantityFilterView.as_view(), name='tp_value_quantity_filter'),
    url(r'^quantity/create/$', QuantityCreateView.as_view(), name='tp_value_quantity_create'),
)
