# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from traceparent.utils import ordered_dict

from .views import UserRetrieveView, UserFilterView, UserCreateView, \
    UserUpdateView, UserLoginView, UserLogoutView, TokenView, \
    UserWhoAmIView, PasswordResetView


class AuthView(APIView):

    def get(self, request):

        data = {
                'user_filter': reverse('tp_auth_user_filter', request=self.request),
                'user_create': reverse('tp_auth_user_create', request=self.request),
                'whoami': reverse('tp_auth_whoami', request=self.request),
                'password_reset': reverse('tp_auth_password_reset', request=self.request),
                'login': reverse('tp_auth_login', request=self.request),
                'logout': reverse('tp_auth_logout', request=self.request),
                'token': reverse('tp_auth_token', request=self.request),
               }

        return Response(ordered_dict(data))


urlpatterns = patterns('',

    # Root
    url(r'^$', AuthView.as_view(), name='tp_auth'),

    # User
    url(r'^user/filter/$', UserFilterView.as_view(), name='tp_auth_user_filter'),
    url(r'^user/create/$', UserCreateView.as_view(), name='tp_auth_user_create'),
    url(r'^user/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/$',
        UserRetrieveView.as_view(), name='tp_auth_user_retrieve'),
    url(r'^user/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/update/$',
        UserUpdateView.as_view(), name='tp_auth_user_update'),

    # Misc
    url(r'^login/$', UserLoginView.as_view(), name='tp_auth_login'),
    url(r'^logout/$', UserLogoutView.as_view(), name='tp_auth_logout'),
    url(r'^token/', TokenView.as_view(), name='tp_auth_token'),
    url(r'^whoami/', UserWhoAmIView.as_view(), name='tp_auth_whoami'),
    url(r'^password_reset/', PasswordResetView.as_view(), name='tp_auth_password_reset'),
)
