# -*- coding: utf-8 -*-
import django_filters

from django.http import HttpResponse
from django.forms import widgets

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, \
    RetrieveDestroyAPIView, RetrieveAPIView
#from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import relations

from traceparent.fields import HyperlinkedFilterField
from traceparent.widgets import MultipleLockedInput

from tp_auth.permissions import IsCreatorOrUser

from .models import Snippet


class SnippetFilter(django_filters.FilterSet):

    creator  = django_filters.CharFilter(lookup_type='exact')
    user     = django_filters.CharFilter(lookup_type='exact')
    mimetype = django_filters.CharFilter(lookup_type='exact')
    slug     = django_filters.CharFilter(lookup_type='iexact')
    type     = django_filters.CharFilter(lookup_type='iexact')

    # Models
    assigned_users      = django_filters.CharFilter(lookup_type='exact')
    assigned_units      = django_filters.CharFilter(lookup_type='exact')
    assigned_quantities = django_filters.CharFilter(lookup_type='exact')

    class Meta:

        model = Snippet
        fields = ('creator', 'user', 'mimetype', 'slug', 'type',
                     'assigned_users', 'assigned_units', 'assigned_quantities',)


class SnippetSerializer(serializers.ModelSerializer):

    url  = serializers.HyperlinkedIdentityField(view_name='tp_metadata_snippet_retrieve') 
    user = serializers.HyperlinkedRelatedField(view_name='tp_auth_user_retrieve')

    class Meta:

        model = Snippet
        fields = ('uuid', 'url', 'user', 'visibility', 'mimetype', 'slug', 'type',
                  'datetime', 'assigned_users', 'assigned_units', 'assigned_quantities',)


class SnippetFilterView(ListAPIView):

    serializer_class = SnippetSerializer
    filter_class     = SnippetFilter
    model            = Snippet


from tp_value.models import Unit, Quantity
from tp_auth.models import User

class SnippetCreateSerializer(serializers.ModelSerializer):

    content             = CharField(widget=widgets.Textarea)
    assigned_users      = relations.ManyPrimaryKeyRelatedField(required=False,
                              widget=MultipleLockedInput(model=User))
    assigned_units      = relations.ManyPrimaryKeyRelatedField(required=False,
                              widget=MultipleLockedInput(model=Unit))
    assigned_quantities = relations.ManyPrimaryKeyRelatedField(required=False,
                              widget=MultipleLockedInput(model=Quantity))

    class Meta:

        model = Snippet
        fields = ('user', 'visibility', 'mimetype', 'slug', 'type', 'content',
                  'assigned_users', 'assigned_units', 'assigned_quantities',)

    def validate_type(self, attrs, source):

        if  attrs[source] == '': attrs[source] = None

        return attrs

    def validate(self, attrs):

        attrs['creator'] = self.context['request'].user
        #raise serializers.ValidationError("Symbolic users cannot have a password.")

        return attrs


class SnippetCreateView(CreateAPIView):

    permission_classes = (IsAuthenticated,) 
    model              = Snippet
    serializer_class   = SnippetCreateSerializer

    def get(self, request, format=None): return Response(None)

    def get_serializer_context(self, *args, **kwargs):

        assigned_user = self.request.GET.get('assigned_users')
        form_initial = {}

        # FIXME: not DRY at all, merge with MultipleLockedInput.
        assigned_user = self.request.GET.get('assigned_users')
        if assigned_user:

            try:

                assigned_user = User.objects.get(pk=assigned_user)
                form_initial.update({'assigned_users': (assigned_user.pk,),})

            except User.DoesNotExist: pass

        # FIXME: not DRY at all, merge with MultipleLockedInput.
        assigned_unit = self.request.GET.get('assigned_units')
        if assigned_unit:

            try:

                assigned_unit = Unit.objects.get(pk=assigned_unit)
                form_initial.update({'assigned_units': (assigned_unit.pk,),})

            except Unit.DoesNotExist: pass

        # FIXME: not DRY at all, merge with MultipleLockedInput.
        assigned_quantity = self.request.GET.get('assigned_quantities')
        if assigned_quantity:

            try:

                assigned_quantity = Quantity.objects.get(pk=assigned_quantity)
                form_initial.update({'assigned_quantities': (assigned_quantity.pk,),})

            except Quantity.DoesNotExist: pass

        c = super(SnippetCreateView, self).get_serializer_context(*args, **kwargs)
        c.update({'form_initial': form_initial})

        return c


class SnippetUpdateView(RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated, IsCreatorOrUser,)
    model              = Snippet
    serializer_class   = SnippetCreateSerializer

    def get(self, request, format=None, *args, **kwargs):

        super(SnippetUpdateView, self).get(request, format=None, *args, **kwargs)

        return Response({'FIXME':
            'https://github.com/tomchristie/django-rest-framework/issues/731'})


class SnippetRetrieveView(RetrieveDestroyAPIView):

    model            = Snippet
    serializer_class = SnippetSerializer
# FIXME: permissions
    #content_object   = None
    #pk_url_kwarg     = 'snippet_pk'

    #def get(self, request, model=None, content_obj_pk=None, *args, **kwargs):

    #    self.content_object = get_object_or_404(model, pk=content_obj_pk)

    #    return super(SnippetRetrieveView, self).get(request, *args, **kwargs)

    #def get_queryset(self):

    #    o_type = ContentType.objects.get_for_model(self.content_object)

    #    return Snippet.objects.filter(content_type__pk=o_type.pk,
    #                                  object_pk=self.content_object.pk)


class SnippetRetrieveContentView(RetrieveAPIView):

    model = Snippet
# FIXME: permissions

    def get(self, request, *args, **kwargs):

        super(SnippetRetrieveContentView, self).get(request, *args, **kwargs)

        return HttpResponse(self.object.content, content_type=self.object.mimetype)
