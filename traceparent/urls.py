# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse


class RootAPIView(APIView):

    def get(self, request):

        return Response({
                         'auth': reverse('tp_auth', request=request),
                         'value': reverse('tp_value', request=request)
                        })


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'traceparent.views.home', name='home'),
    # url(r'^traceparent/', include('traceparent.foo.urls')),
    url(r'^$', RootAPIView.as_view()),
    url(r'^auth/', include('tp_auth.urls')),
    url(r'^value/', include('tp_value.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
