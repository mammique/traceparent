# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .views import UserView, UserCreateView


class AuthView(APIView):

    def get(self, request):

        return Response(
                        {
                         'filter': reverse('tp_auth_user', request=self.request),
                         'create': reverse('tp_auth_user_create', request=self.request),
                         'manage': '',
#                         'login':  reverse('login', request=self.request),
#                         'logout': reverse('logout', request=self.request),
                        }
                       )


#from django.conf.urls import include

urlpatterns = patterns('',
    url(r'^$', AuthView.as_view(), name='tp_auth'),
    url(r'^user/$', UserView.as_view(), name='tp_auth_user'),
    url(r'^user/create/$', UserCreateView.as_view(), name='tp_auth_user_create'),
#    url(r'^token/', 'rest_framework.authtoken.views.obtain_auth_token')
#    url(r'^logout/$', 'django.contrib.auth:logout',),
    #url(r'^auth', include('rest_framework.urls', namespace='rest_framework'))
)


