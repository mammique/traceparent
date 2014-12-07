# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Unit, QuantityStatus, Quantity, Converter


admin.site.register(Unit)
# admin.site.register(QuantityStatus)
admin.site.register(Quantity)
admin.site.register(Converter)
