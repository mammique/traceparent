# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404

from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.compat import patterns, url
from rest_framework.views import APIView

from traceparent.utils import ordered_dict
from traceparent.views import M2MAddView, M2MRemoveView

from .views import bucket_content_nginx #, BucketUpdateView
from .models import Bucket

#class ServeView(APIView):
#
    #def get(self, request):
#
        #data = ordered_dict(
            #{
             #'bucket': reverse('extra_serve_bucket', request=self.request),
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
             #'create': reverse('extra_serve_bucket_create', request=self.request),
             #'filter': reverse('extra_serve_bucket_filter', request=self.request),
            #}
        #)
#
        #return Response(data)


# FIXME: use RetrieveAPIView?
class BucketUpdateUsersRoView(APIView):

    def get(self, request, *args, **kwargs):

        if not args: args = (kwargs['user_pk'], kwargs['bucket_slug'],)

        data = ordered_dict(
            {
             'add':    reverse('extra_serve_bucket_update_users_ro_add', args,
                               request=self.request),
             'remove': reverse('extra_serve_bucket_update_users_ro_remove', args,
                               request=self.request),
            }
        )

        return Response(data)


class BucketM2MAddView(M2MAddView):

    def get_object(self, queryset=None, *args, **kwargs):

        user_pk     = self.kwargs.get('user_pk')
        bucket_slug = self.kwargs.get('bucket_slug')

        # https://github.com/tomchristie/django-rest-framework/blob/b1847412b57b4bc7db39739e0c7c0e8469d3bb48/rest_framework/generics.py#L260
        # Determine the base queryset to use.
        if queryset is None:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            pass  # Deprecation warning

        filter_kwargs = {'user': user_pk, 'slug': bucket_slug}

        try: obj = _get_object_or_404(queryset, **filter_kwargs)
        except (TypeError, ValueError): return Http404

        self.check_object_permissions(self.request, obj)

        return obj


class BucketM2MRemoveView(M2MRemoveView):

    def get_object(self, queryset=None, *args, **kwargs):

        user_pk     = self.kwargs.get('user_pk')
        bucket_slug = self.kwargs.get('bucket_slug')

        # https://github.com/tomchristie/django-rest-framework/blob/b1847412b57b4bc7db39739e0c7c0e8469d3bb48/rest_framework/generics.py#L260
        # Determine the base queryset to use.
        if queryset is None:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            pass  # Deprecation warning

        filter_kwargs = {'user': user_pk, 'slug': bucket_slug}

        try: obj = _get_object_or_404(queryset, **filter_kwargs)
        except (TypeError, ValueError): return Http404

        self.check_object_permissions(self.request, obj)

        return obj


urlpatterns = patterns('django.contrib.auth.views',

    #url(r'^$', ServeView.as_view(), name=''),

    url(r'^bucket/(?P<user_pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/(?P<bucket_slug>[\w]+)/content/(?P<content_path>.*)$',
        bucket_content_nginx, name='extra_serve_bucket_content'),
    url(r'^bucket/(?P<user_pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/(?P<bucket_slug>[\w]+)/update/users_ro/$',
        BucketUpdateUsersRoView.as_view(), name='extra_serve_bucket_update_users_ro'),
    url(r'^bucket/(?P<user_pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/(?P<bucket_slug>[\w]+)/update/users_ro/add/$',
        BucketM2MAddView.as_view(model=Bucket), {'m2m_field': 'users_ro'},
        name='extra_serve_bucket_update_users_ro_add'),
    url(r'^bucket/(?P<user_pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/(?P<bucket_slug>[\w]+)/update/users_ro/remove/$',
        BucketM2MRemoveView.as_view(model=Bucket), {'m2m_field': 'users_ro'},
        name='extra_serve_bucket_update_users_ro_remove'),

)
