# -*- coding: utf-8 -*-
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.compat import patterns, url
from rest_framework.views import APIView

from traceparent.utils import ordered_dict

from .views import bucket_file_nginx #, BucketUpdateView


#class ServeView(APIView):
#
    #def get(self, request):
#
        #data = ordered_dict(
            #{
             #'bucket': reverse('drf_serve_bucket', request=self.request),
            #}
        #)
#
        #return Response(data)
#
#
#class BucketView(APIView):
#
    #def get(self, request):
#
        #data = ordered_dict(
            #{
             #'create': reverse('drf_serve_bucket_create', request=self.request),
             #'filter': reverse('drf_serve_bucket_filter', request=self.request),
            #}
        #)
#
        #return Response(data)


urlpatterns = patterns('django.contrib.auth.views',

    #url(r'^$', ServeView.as_view(), name=''),

    url(r'^bucket/(?P<user_pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/(?P<bucket_slug>[\w]+)/(?P<filename>.*)$',
        bucket_file_nginx, name='drf_serve_bucket_update'),
    #url(r'^bucket/(?P<user_pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/(?P<bucket_slug>[\w]+)/update/$',
        #ServeBucketUpdateView.as_view(), name='drf_serve_bucket_update'),
)
