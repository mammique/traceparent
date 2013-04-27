# -*- coding: utf-8 -*-
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.compat import patterns, url
from rest_framework.views import APIView

from traceparent.utils import ordered_dict

from .views import bucket_content_nginx #, BucketUpdateView


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

    url(r'^bucket/(?P<user_pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/(?P<bucket_slug>[\w]+)/content/(?P<content_path>.*)$',
        bucket_content_nginx, name='drf_serve_bucket_content'),
    #url(r'^bucket/(?P<user_pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/(?P<bucket_slug>[\w]+)/update/users_ro/$',
        #ScopeUpdateQuantitiesView.as_view(), name='drf_serve_bucket_update_users_ro'),
    #url(r'^bucket/(?P<user_pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/(?P<bucket_slug>[\w]+)/update/users_ro/add/$',
        #M2MAddView.as_view(model=Scope), {'m2m_field': 'users_ro'},
        #name='drf_serve_bucket_update_users_ro_add'),
    #url(r'^bucket/(?P<user_pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/(?P<bucket_slug>[\w]+)/update/users_ro/remove/$',
        #M2MRemoveView.as_view(model=Scope), {'m2m_field': 'users_ro'},
        #name='drf_serve_bucket_update_users_ro_remove'),

)
