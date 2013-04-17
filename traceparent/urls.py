# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from traceparent.utils import ordered_dict


class RootAPIView(APIView):

    def get_name(self): return settings.PROJECT_NAME

    def get(self, request):

        data = ordered_dict(
            {
             'auth':     reverse('tp_auth',     request=request),
             'value':    reverse('tp_value',    request=request),
             'metadata': reverse('tp_metadata', request=request),
             'monitor':  reverse('tp_monitor',  request=request),
            }
        )

        return Response(data)


#class ExtraAPIView(APIView):
#
    #def get(self, request):
#
        #data = ordered_dict(
            #{
             #'serve':    reverse('drf_serve', request=request),
            #}
        #)
        #
        #return Response(data)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'traceparent.views.home', name='home'),
    # url(r'^traceparent/', include('traceparent.foo.urls')),
    url(r'^$',         RootAPIView.as_view()),
    url(r'^auth/',     include('tp_auth.urls')),
    url(r'^value/',    include('tp_value.urls')),
    url(r'^metadata/', include('tp_metadata.urls')),
    url(r'^monitor/',  include('tp_monitor.urls')),

    # url(r'^extra/', ExtraAPIView.as_view()),
    url(r'^extra/serve/',  include('drf_serve.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
