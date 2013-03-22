# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Scope, Counter, Mark


admin.site.register(Scope)
admin.site.register(Counter)
admin.site.register(Mark)
