# -*- coding: utf-8 -*-
from rest_framework.filters import DjangoFilterBackend


class NoneDjangoFilterBackend(DjangoFilterBackend):

    # https://github.com/tomchristie/django-rest-framework/blob/b052c92ac38f90e5b56cfd128cd4a488713c048e/rest_framework/filters.py#L54
    def filter_queryset(self, request, queryset, view):

        filter_class = self.get_filter_class(view)

        if filter_class:

            dic = dict(filter(lambda x: x[0] in filter_class._meta.fields and x[1] != '',
                request.QUERY_PARAMS.items()))

            if not len(dic): return queryset.none()

            view.filter_instance = filter_class(dic, queryset=queryset)

            return view.filter_instance.qs

        return queryset
