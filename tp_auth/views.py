# -*- coding: utf-8 -*-
import django_filters
from django.contrib.auth.hashers import make_password, UNUSABLE_PASSWORD
from django.forms import widgets

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework import serializers
#from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.fields import CharField, EmailField#, BooleanField
#from rest_framework.relations import HyperlinkedRelatedField
from rest_framework import status

from traceparent.utils import blanks_prune

from .models import User

# Bienvenue Email

class UserCreateSerializer(serializers.ModelSerializer):

    request = None
    password = CharField(required=False, blank=True, widget=widgets.PasswordInput)
    email = EmailField(required=False) # FIXME: help_text
#    created_by_me = BooleanField(default=False)

    class Meta:

        model = User
        fields = ('name', 'email', 'password',)

    def __init__(self, *args, **kwargs):

        self.request = kwargs['context']['request']

        return super(UserCreateSerializer, self).__init__(*args, **kwargs)

    def validate_email(self, attrs, source):

        value = attrs[source]

        if value and User.objects.filter(email__iexact=value).count():
            raise serializers.ValidationError("Email not available.")

        return attrs

    def validate_password(self, attrs, source):

        attrs[source] = make_password(attrs[source])

        return attrs

    def validate_name(self, attrs, source):

        attrs[source] = blanks_prune(attrs[source])

        return attrs

    def validate(self, attrs):

        attrs['creator'] = self.request.user \
            if self.request.user.is_authenticated() else None
#            if self.request.user.is_authenticated() and attrs['created_by_me'] else None

#        del attrs['created_by_me']

        if not attrs['email']:

            if not attrs['creator']:
                 raise serializers.ValidationError(
                     "You must be authenticated to create symbolic users.")
#                     "You must be authenticated and be the creator to create symbolic users.")

            if not attrs['name']:
                raise serializers.ValidationError("Symbolic users must have a name.")

            if attrs['password'] != UNUSABLE_PASSWORD:
                raise serializers.ValidationError("Symbolic users cannot have a password.")

        return attrs


class UserCreateView(CreateAPIView):

    serializer_class = UserCreateSerializer
    model = User

    def get(self, request, format=None): return Response(None)

    def create(self, request, *args, **kwargs):

        r = super(UserCreateView, self).create(request, *args, **kwargs)

        if r.status_code == status.HTTP_201_CREATED:
            return Response(UserSerializer(self.object).data, status=status.HTTP_201_CREATED)

        return r


class UserFilter(django_filters.FilterSet):

    uuid    = django_filters.CharFilter(lookup_type='exact')
    name    = django_filters.CharFilter(lookup_type='icontains')
    email   = django_filters.CharFilter(lookup_type='iexact')
    creator = django_filters.CharFilter(lookup_type='exact')

    class Meta:

        model = User
        fields = ('uuid', 'name', 'email', 'creator',)


class UserSerializer(serializers.ModelSerializer):

    #url = HyperlinkedRelatedField(view_name='tp_auth_user_retrieve') #many=, read_only=True,

    class Meta:

        model = User
        fields = ('uuid', 'name',) # 'url',)


class UserFilterView(ListAPIView):

    serializer_class = UserSerializer
    model = User
    filter_class = UserFilter


class UserRetrieveView(RetrieveAPIView):

    serializer_class = UserSerializer
    model = User
