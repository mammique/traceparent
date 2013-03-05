# -*- coding: utf-8 -*-
from django.conf import settings as project_settings


def settings(request): return {'settings': project_settings}
