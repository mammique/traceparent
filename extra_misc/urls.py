# -*- coding: utf-8 -*-
from rest_framework.compat import patterns, url

from .views import client_headers_bounce


urlpatterns = patterns('django.contrib.auth.views',

    url(r'^client_headers_bounce/', client_headers_bounce),
)
