# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from traceparent.utils import ordered_dict
from traceparent.views import M2MAddView, M2MRemoveView

from .models import Scope
from .views import ScopeFilterView, ScopeRetrieveView, \
                       ScopeCreateView, \
                   CounterFilterView, CounterRetrieveView, \
                       CounterCreateView, CounterUpdateView, \
                   MarkFilterView, MarkRetrieveView, \
                       MarkCreateView, MarkUpdateView, \
                   ResultSumFilterView


class MonitorView(APIView):

    def get(self, request):

        data = ordered_dict(
            {
             'scope':   reverse('tp_monitor_scope', request=self.request),
             'counter': reverse('tp_monitor_counter', request=self.request),
             'mark':    reverse('tp_monitor_mark', request=self.request),
             'result':  reverse('tp_monitor_result', request=self.request),
            }
        )
        
        return Response(data)


class ScopeView(APIView):

    def get(self, request):

        data = ordered_dict(
            {
             'create': reverse('tp_monitor_scope_create', request=self.request),
             'filter': reverse('tp_monitor_scope_filter', request=self.request),
            }
        )

        return Response(data)


# FIXME: use RetrieveAPIView?
class ScopeUpdateQuantitiesView(APIView):

    def get(self, request, *args, **kwargs):

        if not args: args = (kwargs['pk'],)

        data = ordered_dict(
            {
             'add':    reverse('tp_monitor_scope_update_quantities_add', args,
                               request=self.request),
             'remove': reverse('tp_monitor_scope_update_quantities_remove', args,
                               request=self.request),
            }
        )

        return Response(data)


class CounterView(APIView):

    def get(self, request):

        data = ordered_dict(
            {
             'create': reverse('tp_monitor_counter_create', request=self.request),
             'filter': reverse('tp_monitor_counter_filter', request=self.request),
            }
        )

        return Response(data)


class MarkView(APIView):

    def get(self, request):

        data = ordered_dict(
            {
             'create': reverse('tp_monitor_mark_create', request=self.request),
             'filter': reverse('tp_monitor_mark_filter', request=self.request),
            }
        )

        return Response(data)


class ResultView(APIView):

    def get(self, request):

        data = ordered_dict(
            {
             'sum': reverse('tp_monitor_result_sum', request=self.request),
            }
        )

        return Response(data)


class ResultSumView(APIView):

    def get(self, request):

        data = ordered_dict(
            {
             'filter': reverse('tp_monitor_result_sum_filter', request=self.request),
            }
        )

        return Response(data)


urlpatterns = patterns('',

    # Root
    url(r'^$', MonitorView.as_view(), name='tp_monitor'),

    # Scope
    url(r'^scope/$', ScopeView.as_view(), name='tp_monitor_scope'),
    url(r'^scope/filter/$', ScopeFilterView.as_view(), name='tp_monitor_scope_filter'),
    url(r'^scope/create/$', ScopeCreateView.as_view(), name='tp_monitor_scope_create'),
    url(r'^scope/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/$',
        ScopeRetrieveView.as_view(), name='tp_monitor_scope_retrieve'),
    url(r'^scope/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/quantities/$',
        ScopeUpdateQuantitiesView.as_view(), name='tp_monitor_scope_update_quantities'),
    url(r'^scope/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/quantities/add/$',
        M2MAddView.as_view(model=Scope), {'m2m_field': 'quantities'},
        name='tp_monitor_scope_update_quantities_add'),
    url(r'^scope/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/quantities/remove/$',
        M2MRemoveView.as_view(model=Scope), {'m2m_field': 'quantities'},
        name='tp_monitor_scope_update_quantities_remove'),

    # Counter
    url(r'^counter/$', CounterView.as_view(), name='tp_monitor_counter'),
    url(r'^counter/filter/$', CounterFilterView.as_view(), name='tp_monitor_counter_filter'),
    url(r'^counter/create/$', CounterCreateView.as_view(), name='tp_monitor_counter_create'),
    url(r'^counter/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/$',
        CounterRetrieveView.as_view(), name='tp_monitor_counter_retrieve'),
    url(r'^counter/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/$',
        CounterUpdateView.as_view(), name='tp_monitor_counter_update'),

    # Mark
    url(r'^mark/$', MarkView.as_view(), name='tp_monitor_mark'),
    url(r'^mark/filter/$', MarkFilterView.as_view(), name='tp_monitor_mark_filter'),
    url(r'^mark/create/$', MarkCreateView.as_view(), name='tp_monitor_mark_create'),
    url(r'^mark/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/$',
        MarkRetrieveView.as_view(), name='tp_monitor_mark_retrieve'),
    url(r'^mark/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/$',
        MarkUpdateView.as_view(), name='tp_monitor_mark_update'),

    # Result
    url(r'^result/$', ResultView.as_view(), name='tp_monitor_result'),
    url(r'^result/sum/$', ResultSumView.as_view(), name='tp_monitor_result_sum'),
    url(r'^result/sum/filter/$', ResultSumFilterView.as_view(), name='tp_monitor_result_sum_filter'),
)
