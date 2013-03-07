# -*- coding: utf-8 -*-
import django_filters
from django.contrib.auth.hashers import make_password, UNUSABLE_PASSWORD
from django.forms import widgets
from django.contrib.auth import login, logout, authenticate

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, \
    RetrieveAPIView, CreateAPIView
from rest_framework import serializers
from rest_framework.authtoken.models import Token
#from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.fields import CharField, EmailField #, BooleanField
#from rest_framework.relations import HyperlinkedRelatedField
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from traceparent.utils import blanks_prune
from traceparent.mixins import RequestSerializerMixin

from .models import User

# Bienvenue Email

class UserAlterSerializerBase(RequestSerializerMixin, serializers.ModelSerializer):

    password = CharField(required=False, blank=True, widget=widgets.PasswordInput)
    email    = EmailField(required=False) # FIXME: help_text

    class Meta:

        model = User
        fields = ('uuid', 'name', 'email', 'password', 'date_joined', 'is_active',)
        read_only_fields = ('uuid', 'date_joined', 'is_active',)

    @property
    def data(self):

        data = super(UserAlterSerializerBase, self).data.copy()
        del data['password']

        return data

    def validate_email(self, attrs, source):

        value = attrs[source]

        if not self.object or value != self.object.email:

            if value and User.objects.filter(email__iexact=value).count():
                raise serializers.ValidationError("Email not available.")

        return attrs

    def validate_password(self, attrs, source):

        attrs[source] = make_password(attrs[source])

        if self.object and attrs[source] == UNUSABLE_PASSWORD:
            attrs[source] = self.object.password

        return attrs

    def validate_name(self, attrs, source):

        attrs[source] = blanks_prune(attrs[source])

        return attrs


class UserCreateSerializer(UserAlterSerializerBase):

    def validate(self, attrs):

        attrs['creator'] = self.request.user \
            if self.request.user.is_authenticated() else None

        if not attrs['email']:

            if not attrs['creator']:
                 raise serializers.ValidationError(
                     "You must be authenticated to create symbolic users.")

            if not attrs['name']:
                raise serializers.ValidationError("Symbolic users must have a name.")

            if attrs['password'] != UNUSABLE_PASSWORD:
                raise serializers.ValidationError("Symbolic users cannot have a password.")

        return attrs

class UserCreateView(CreateAPIView):

    serializer_class = UserCreateSerializer
    model            = User

    def get(self, request, format=None): return Response(None)

    def create(self, request, *args, **kwargs):

        r = super(UserCreateView, self).create(request, *args, **kwargs)

        if r.status_code == status.HTTP_201_CREATED:
            return Response(UserManageSerializer(self.object).data,
                status=status.HTTP_201_CREATED)

        return r


class UserManageSerializer(UserAlterSerializerBase):

    email = EmailField(required=True)

class UserManageView(RetrieveUpdateAPIView):

    serializer_class   = UserManageSerializer
    model              = User
    permission_classes = (IsAuthenticated,)

    # https://github.com/tomchristie/django-rest-framework/blob/f5a0275547ad264c8a9b9aa2a45cc461723a4f11/rest_framework/generics.py#L129
    def get_object(self, queryset=None):

        obj = self.request.user
        self.check_object_permissions(self.request, obj)

        return obj

    def update(self, request, *args, **kwargs):

        r = super(UserManageView, self).update(request, *args, **kwargs)

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


class NotBlankBooleanField(serializers.Field):

    def field_to_native(self, obj, field_name):
        return getattr(obj, 'email', None) == ''


class UserSerializer(serializers.ModelSerializer):

    symbolic = NotBlankBooleanField()
    #url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:

        model = User
        fields = ('uuid', 'name', 'symbolic',) #, 'url',)


class UserFilterView(ListAPIView):

    serializer_class = UserSerializer
    model            = User
    filter_class     = UserFilter


class UserRetrieveView(RetrieveAPIView):

    serializer_class = UserSerializer
    model            = User


class UserLoginSerializer(RequestSerializerMixin, serializers.Serializer):

    _user    = None
    email    = EmailField(required=True)
    password = CharField(required=True, widget=widgets.PasswordInput)

    def validate(self, attrs):

        self._user = authenticate(username=attrs['email'], password=attrs['password'])

        if self._user is None:
            raise serializers.ValidationError("Email and password don't match.")

        return attrs

    def restore_object(self, attrs, instance=None): return self._user



class UserLoginView(CreateAPIView):

    serializer_class = UserLoginSerializer

    def get(self, request, format=None): return Response(None)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            
            login(self.request, serializer.object)
 
            return Response({'detail': 'Log in successful'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):

    def get(self, request, format=None):

        logout(request)

        return Response({'detail': 'Log out successful'})


class TokenView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None): return Response(None)

    def post(self, request):

        token, created = Token.objects.get_or_create(user=request.user)

        return Response({'token': token.key})
