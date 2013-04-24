# -*- coding: utf-8 -*-
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.compat import patterns, url
from rest_framework.views import APIView

from traceparent.utils import ordered_dict
from traceparent.views import M2MAddView, M2MRemoveView

from .models import Snippet
from .views import SnippetFilterView, SnippetCreateView, \
                       SnippetUpdateView, SnippetRetrieveView

class MetadataView(APIView):

    def get(self, request):

        data = ordered_dict(
            {
             'snippet': reverse('tp_metadata_snippet', request=self.request),
            }
        )

        return Response(data)


class SnippetView(APIView):

    def get(self, request):

        data = ordered_dict(
            {
             'create': reverse('tp_metadata_snippet_create', request=self.request),
             'filter': reverse('tp_metadata_snippet_filter', request=self.request),
            }
        )

        return Response(data)


# FIXME: use RetrieveAPIView?
class SnippetUpdateAssignedUsersView(APIView):

    def get(self, request, *args, **kwargs):

        if not args: args = (kwargs['pk'],)

        data = ordered_dict(
            {
             'add':    reverse('tp_metadata_snippet_update_assigned_users_add', args,
                               request=self.request),
             'remove': reverse('tp_metadata_snippet_update_assigned_users_remove', args,
                               request=self.request),
            }
        )

        return Response(data)


# FIXME: use RetrieveAPIView?
class SnippetUpdateAssignedUnitsView(APIView):

    def get(self, request, *args, **kwargs):

        if not args: args = (kwargs['pk'],)

        data = ordered_dict(
            {
             'add':    reverse('tp_metadata_snippet_update_assigned_units_add', args,
                               request=self.request),
             'remove': reverse('tp_metadata_snippet_update_assigned_units_remove', args,
                               request=self.request),
            }
        )

        return Response(data)


# FIXME: use RetrieveAPIView?
class SnippetUpdateAssignedQuantitiesView(APIView):

    def get(self, request, *args, **kwargs):

        if not args: args = (kwargs['pk'],)

        data = ordered_dict(
            {
             'add':    reverse('tp_metadata_snippet_update_assigned_quantities_add', args,
                               request=self.request),
             'remove': reverse('tp_metadata_snippet_update_assigned_quantities_remove', args,
                               request=self.request),
            }
        )

        return Response(data)


# FIXME: use RetrieveAPIView?
class SnippetUpdateAssignedScopesView(APIView):

    def get(self, request, *args, **kwargs):

        if not args: args = (kwargs['pk'],)

        data = ordered_dict(
            {
             'add':    reverse('tp_metadata_snippet_update_assigned_scopes_add', args,
                               request=self.request),
             'remove': reverse('tp_metadata_snippet_update_assigned_scopes_remove', args,
                               request=self.request),
            }
        )

        return Response(data)


# FIXME: use RetrieveAPIView?
class SnippetUpdateAssignedCountersView(APIView):

    def get(self, request, *args, **kwargs):

        if not args: args = (kwargs['pk'],)

        data = ordered_dict(
            {
             'add':    reverse('tp_metadata_snippet_update_assigned_counters_add', args,
                               request=self.request),
             'remove': reverse('tp_metadata_snippet_update_assigned_counters_remove', args,
                               request=self.request),
            }
        )

        return Response(data)


# FIXME: use RetrieveAPIView?
class SnippetUpdateAssignedMarksView(APIView):

    def get(self, request, *args, **kwargs):

        if not args: args = (kwargs['pk'],)

        data = ordered_dict(
            {
             'add':    reverse('tp_metadata_snippet_update_assigned_marks_add', args,
                               request=self.request),
             'remove': reverse('tp_metadata_snippet_update_assigned_marks_remove', args,
                               request=self.request),
            }
        )

        return Response(data)


urlpatterns = patterns('',

    url(r'^$', MetadataView.as_view(), name='tp_metadata'),

    # Snippet
    url(r'^snippet/$', SnippetView.as_view(), name='tp_metadata_snippet'),

    url(r'^snippet/filter/$', SnippetFilterView.as_view(), name='tp_metadata_snippet_filter'),
    url(r'^snippet/create/$', SnippetCreateView.as_view(), name='tp_metadata_snippet_create'),

    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/$',
        SnippetRetrieveView.as_view(), name='tp_metadata_snippet_retrieve'),
    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/$',
        SnippetUpdateView.as_view(), name='tp_metadata_snippet_update'),
    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/content$',
        SnippetRetrieveView.as_view(), {'serve_content': True},
        name='tp_metadata_snippet_content',),

    # M2M Add/Remove

    # Assigned users
    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/assigned_users/$',
        SnippetUpdateAssignedUsersView.as_view(), name='tp_metadata_snippet_update_assigned_users'),
    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/assigned_users/add/$',
        M2MAddView.as_view(model=Snippet), {'m2m_field': 'assigned_users'},
        name='tp_metadata_snippet_update_assigned_users_add'),
    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/assigned_users/remove/$',
        M2MRemoveView.as_view(model=Snippet), {'m2m_field': 'assigned_users'},
        name='tp_metadata_snippet_update_assigned_users_remove'),

    # Assigned units
    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/assigned_units/$',
        SnippetUpdateAssignedUnitsView.as_view(), name='tp_metadata_snippet_update_assigned_units'),
    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/assigned_units/add/$',
        M2MAddView.as_view(model=Snippet), {'m2m_field': 'assigned_units'},
        name='tp_metadata_snippet_update_assigned_units_add'),
    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/assigned_units/remove/$',
        M2MRemoveView.as_view(model=Snippet), {'m2m_field': 'assigned_units'},
        name='tp_metadata_snippet_update_assigned_units_remove'),

    # Assigned quantities
    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/assigned_quantities/$',
        SnippetUpdateAssignedQuantitiesView.as_view(), name='tp_metadata_snippet_update_assigned_quantities'),
    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/assigned_quantities/add/$',
        M2MAddView.as_view(model=Snippet), {'m2m_field': 'assigned_quantities'},
        name='tp_metadata_snippet_update_assigned_quantities_add'),
    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/assigned_quantities/remove/$',
        M2MRemoveView.as_view(model=Snippet), {'m2m_field': 'assigned_quantities'},
        name='tp_metadata_snippet_update_assigned_quantities_remove'),

    # Assigned scopes
    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/assigned_scopes/$',
        SnippetUpdateAssignedScopesView.as_view(), name='tp_metadata_snippet_update_assigned_scopes'),
    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/assigned_scopes/add/$',
        M2MAddView.as_view(model=Snippet), {'m2m_field': 'assigned_scopes'},
        name='tp_metadata_snippet_update_assigned_scopes_add'),
    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/assigned_scopes/remove/$',
        M2MRemoveView.as_view(model=Snippet), {'m2m_field': 'assigned_scopes'},
        name='tp_metadata_snippet_update_assigned_scopes_remove'),

    # Assigned counters
    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/assigned_counters/$',
        SnippetUpdateAssignedQuantitiesView.as_view(), name='tp_metadata_snippet_update_assigned_counters'),
    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/assigned_counters/add/$',
        M2MAddView.as_view(model=Snippet), {'m2m_field': 'assigned_counters'},
        name='tp_metadata_snippet_update_assigned_counters_add'),
    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/assigned_counters/remove/$',
        M2MRemoveView.as_view(model=Snippet), {'m2m_field': 'assigned_counters'},
        name='tp_metadata_snippet_update_assigned_counters_remove'),

    # Assigned marks
    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/assigned_marks/$',
        SnippetUpdateAssignedQuantitiesView.as_view(), name='tp_metadata_snippet_update_assigned_marks'),
    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/assigned_marks/add/$',
        M2MAddView.as_view(model=Snippet), {'m2m_field': 'assigned_marks'},
        name='tp_metadata_snippet_update_assigned_marks_add'),
    url(r'^snippet/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/assigned_marks/remove/$',
        M2MRemoveView.as_view(model=Snippet), {'m2m_field': 'assigned_marks'},
        name='tp_metadata_snippet_update_assigned_marks_remove'),
)
