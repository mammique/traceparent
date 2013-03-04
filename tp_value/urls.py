# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .views import UnitView, QuantityView


class ValueView(APIView):

    def get(self, request):

        return Response(
                        {
                         'unit': reverse('tp_value_unit', request=self.request),
                         'quantity': reverse('tp_value_quantity', request=self.request),
                        }
                       )


urlpatterns = patterns('',
    url(r'^$', ValueView.as_view(), name='tp_value'),
    url(r'^unit/$', UnitView.as_view(), name='tp_value_unit'),
    url(r'^quantity/$', QuantityView.as_view(), name='tp_value_quantity'),
)
