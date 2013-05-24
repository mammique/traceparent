# -*- coding: utf-8 -*-
import django_filters, urllib
from django.contrib.auth.hashers import make_password, UNUSABLE_PASSWORD
from django.forms import widgets
from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout, authenticate
from django.conf import settings
from django.http import HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, \
     RetrieveAPIView, CreateAPIView
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.fields import CharField, EmailField, BooleanField
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse

from traceparent.utils import blanks_prune
from traceparent.mixins import DescActionMixin
from traceparent.fields import HyperlinkedFilterField

from .permissions import IsCreatorOrUser
from .models import User, LoginToken


class NotBlankBooleanField(serializers.Field):

    def field_to_native(self, obj, field_name):
        return getattr(obj, self.source, None) == ''


class UserSerializerBase(serializers.ModelSerializer):

    url      = serializers.HyperlinkedIdentityField(view_name='tp_auth_user_retrieve')
    symbolic = NotBlankBooleanField(source='email')


class UserRoLightSerializer(UserSerializerBase):

    class Meta:

        model  = User
        fields = ['uuid', 'name', 'symbolic', 'url',]


class UserRoFullSerializer(UserRoLightSerializer):

    assigned_metadata_snippets = \
        HyperlinkedFilterField(view_name='tp_metadata_snippet_filter',
                  lookup_params={'assigned_users': 'pk'},
                  lookup_test=lambda o: o.assigned_metadata_snippets.all().count() != 0,
                  # querystring_params={'assigned_intersect': ''},
        )

    class Meta:

        model  = UserRoLightSerializer.Meta.model
        fields = UserRoLightSerializer.Meta.fields + \
                     ['email_md5', 'date_joined', 'is_active', 'assigned_metadata_snippets',]


class UserFilter(django_filters.FilterSet):

    uuid    = django_filters.CharFilter(lookup_type='exact')
    name    = django_filters.CharFilter(lookup_type='icontains')
    email   = django_filters.CharFilter(lookup_type='iexact')
    creator = django_filters.CharFilter(lookup_type='exact')
    # TODO: prevent private quantities from being fetched.

    # Metadata
    assigned_metadata_snippets = django_filters.CharFilter(lookup_type='exact')

    class Meta:

        model = User
        fields = ('uuid', 'name', 'email', 'creator', 'assigned_metadata_snippets',)


class UserFilterView(ListAPIView):

    serializer_class = UserRoLightSerializer
    model            = User
    filter_class     = UserFilter


class UserRetrieveView(DescActionMixin, RetrieveAPIView):

    serializer_class = UserRoFullSerializer
    model            = User
    description_actions = (
                           ('Add new metadata', lambda x: '%s?assigned_users=%s' % \
                               (reverse('tp_metadata_snippet_create'), x.pk)),
                           ('Update', lambda x: reverse('tp_auth_user_update', (x.pk,))),
                           )


class UserWhoAmIView(UserRetrieveView):

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated(): data = self.get_serializer(request.user).data
        else: data = None

        return Response(data)


class UserAlterSerializerBase(UserSerializerBase):

    password = CharField(required=False, blank=True, widget=widgets.PasswordInput)
    email    = EmailField(required=False) # FIXME: help_text

    class Meta:

        model = User
        fields = UserRoLightSerializer.Meta.fields + \
                     ['email_md5', 'date_joined', 'is_active', 'email', 'password',]
        read_only_fields = ('email_md5', 'uuid', 'date_joined', 'is_active',)

    # FIXME: move to to_native()?
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

        # FIXME: move to view's pre_save()?
        attrs['creator'] = self.context['request'].user \
            if self.context['request'].user.is_authenticated() else None

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

            user = self.object

            if user.email:

                if user.creator:

                    if not user.creator.name: creator = user.creator.email
                    else: creator = '%s <%s>' % (user.creator.name, user.creator.email)

                else: creator = None

                subject = "[%s] Welcome!" % settings.PROJECT_NAME
                if creator: subject += ' (via %s)' % creator # FIXME: replace by profile URL.

                body = """Welcome to %(pname)s.%(creator)s\n\n--\n%(purl)s""" % \
                    {'pname': settings.PROJECT_NAME,
                     'creator': "\n\nYour account has been created by %s." % \
                          creator if creator else '',
                     'purl': settings.PROJECT_URL}

                user.email_user(subject, body)

            return Response(self.get_serializer(user).data, status=status.HTTP_201_CREATED)
            
        return r


class UserUpdateSerializer(UserAlterSerializerBase):

    email = EmailField(required=True)

class UserUpdateView(RetrieveUpdateAPIView):

    serializer_class   = UserUpdateSerializer
    model              = User
    permission_classes = (IsAuthenticated, IsCreatorOrUser)


class UserLoginSerializer(serializers.Serializer):

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

    def get(self, request, format=None, redirect_field_name=REDIRECT_FIELD_NAME):

        token_hash = request.REQUEST.get('login_token', None)

        if token_hash:

            try:

                token = LoginToken.objects.get(pk=request.REQUEST.get('login_token', None))
                token.user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(self.request, token.user)
                token.delete()

                redirect = request.REQUEST.get(redirect_field_name, None)
                if redirect and redirect != request.META['SCRIPT_NAME'] + \
                    request.META['PATH_INFO']: return HttpResponseRedirect(redirect)

            except:

                # FIXME: Don't assume that the user got its token from password reset.
                return Response(
                    {'detail': "Invalid token, please reset your password again at: %s" % \
                        reverse('tp_auth_password_reset', request=self.request)},
                    status=status.HTTP_400_BAD_REQUEST)

        return Response(None)

    def post(self, request, redirect_field_name=REDIRECT_FIELD_NAME, *args, **kwargs):

        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            
            login(self.request, serializer.object)

            redirect = request.REQUEST.get(redirect_field_name, None)
            if redirect and redirect != request.META['SCRIPT_NAME'] + \
                request.META['PATH_INFO']: return HttpResponseRedirect(redirect)

            return Response({'detail': 'Log in successful'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):

    def get(self, request, format=None, redirect_field_name=REDIRECT_FIELD_NAME):

        logout(request)

        redirect = request.REQUEST.get(redirect_field_name, None)
        if redirect and redirect != request.META['SCRIPT_NAME'] + \
            request.META['PATH_INFO']: return HttpResponseRedirect(redirect)

        return Response({'detail': 'Log out successful'})


class TokenSerializer(serializers.Serializer):

    generate_new = BooleanField(required=True)


class TokenView(CreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class =TokenSerializer

    def get(self, request, format=None):

        token, created = Token.objects.get_or_create(user=request.user)

        return Response({'token': token.key})

    def post(self, request, format=None):

        s = self.get_serializer(data=request.DATA)

        if s.is_valid():

            if s.data['generate_new']: Token.objects.filter(user=request.user).delete()

            return self.get(request, format=format)

        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetSerializer(serializers.Serializer):

    email = EmailField(required=True)


class PasswordResetView(CreateAPIView):

    serializer_class = PasswordResetSerializer

    def get(self, request, format=None): return Response(None)

    def create(self, request, format=None):

        s = self.get_serializer(data=request.DATA)

        if s.is_valid():

            email = s.data['email']

            try:

                user = User.objects.get(email=email)

                LoginToken.objects.filter(user=request.user).delete()
                token, created = LoginToken.objects.get_or_create(user=user)

                ui_uri = '%s%s' % (settings.TP_EXTERNAL_UI_URI, reverse('tp_auth_user_update', (user.pk,)))

                body = """You have requested to reset your password on %s.\n\n""" \
                       """To do so, please visit the following address: """ \
                       """%s?login_token=%s&next=%s\n\n--\n%s""" % \
                           (settings.PROJECT_NAME,
                            reverse('tp_auth_login', request=self.request),
                            token.pk, urllib.quote(ui_uri),
                            settings.PROJECT_URL)

                user.email_user("[%s] Password reset" % settings.PROJECT_NAME, body)

            except 1: pass

        #token, created = Token.objects.get_or_create(user=request.user)

            return Response({'detail': 'Password reset information has been sent to %s.' % \
                email})

        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
