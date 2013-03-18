# -*- coding: utf-8 -*-
from rest_framework import permissions

from .models import User


class ObjectIsPublic(permissions.BasePermission):

    def has_object_permission(self, request, view, o):

        return o.visibility == 'public'


class IsCreatorOrUser(permissions.BasePermission):

    def has_object_permission(self, request, view, o):

        if hasattr(o, 'creator') and o.creator == request.user: return True

        if isinstance(o, User): user = o
        else: user = getattr(o, 'user', None)

        if user and user == request.user: return True

        return False
