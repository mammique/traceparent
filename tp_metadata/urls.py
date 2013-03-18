# -*- coding: utf-8 -*-
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.compat import patterns, url
from rest_framework.views import APIView

from traceparent.utils import ordered_dict

from .views import SnippetFilterView, SnippetCreateView, \
                       SnippetUpdateView, SnippetRetrieveView


class MetadataView(APIView):

    def get(self, request):

        data = ordered_dict(
            {
             'create': reverse('tp_metadata_snippet_create', request=self.request),
             'filter': reverse('tp_metadata_snippet_filter', request=self.request),
            }
        )

        return Response(data)

urlpatterns = patterns('django.contrib.auth.views',

    url(r'^$', MetadataView.as_view(), name='tp_metadata_snippet'),

    url(r'^filter/$', SnippetFilterView.as_view(), name='tp_metadata_snippet_filter'),
    url(r'^create/$', SnippetCreateView.as_view(), name='tp_metadata_snippet_create'),

    url(r'^(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/$',
        SnippetRetrieveView.as_view(), name='tp_metadata_snippet_retrieve'),
    url(r'^(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/$',
        SnippetUpdateView.as_view(), name='tp_metadata_snippet_update'),
    url(r'^(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/content$',
        SnippetRetrieveView.as_view(), {'serve_content': True},
        name='tp_metadata_snippet_content',),
)
