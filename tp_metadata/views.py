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
from rest_framework.reverse import reverse

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
    #assigned_quantities = django_filters.ModelMultipleChoiceFilter()


    class Meta:

        model = Snippet
        fields = ('creator', 'user', 'mimetype', 'slug', 'type',
                  'assigned_users', 'assigned_units', 'assigned_quantities',)


class SnippetContentField(serializers.HyperlinkedIdentityField):

    def field_to_native(self, o, *args, **kwargs):

        if 'content_nested' in self.context.get('request').GET: return o.content

        return super(SnippetContentField, self).field_to_native(o, *args, **kwargs)


class SnippetRoLightSerializer(serializers.ModelSerializer):

    url     = serializers.HyperlinkedIdentityField(view_name='tp_metadata_snippet_retrieve') 
    user    = serializers.HyperlinkedRelatedField(view_name='tp_auth_user_retrieve')
    content = SnippetContentField(view_name='tp_metadata_snippet_content')

    class Meta:

        model  = Snippet
        fields = ['uuid', 'url', 'user', 'visibility', 'mimetype', 'slug', 'type',
                  'content', 'datetime',]


class SnippetRoFullSerializer(SnippetRoLightSerializer):

    assigned_users = HyperlinkedFilterField(view_name='tp_auth_user_filter',
                  lookup_params={'assigned_metadata_snippets': 'pk'},
                  lookup_test=lambda o: o.assigned_users.all().count() != 0)
    assigned_units = HyperlinkedFilterField(view_name='tp_value_unit_filter',
                  lookup_params={'assigned_metadata_snippets': 'pk'},
                  lookup_test=lambda o: o.assigned_units.all().count() != 0)
    assigned_quantities = HyperlinkedFilterField(view_name='tp_value_quantity_filter',
                  lookup_params={'assigned_metadata_snippets': 'pk'},
                  lookup_test=lambda o: o.assigned_quantities.all().count() != 0)

    #assigned_retrieve = {
    #                     'assigned_users': 'tp_auth_user_retrieve',
    #                     'assigned_units': 'tp_value_unit_retrieve',
    #                     'assigned_quantities': 'tp_value_quantity_retrieve',
    #                    }

    class Meta:

        model  = SnippetRoLightSerializer.Meta.model
        fields = SnippetRoLightSerializer.Meta.fields + \
                     ['assigned_users', 'assigned_units', 'assigned_quantities',]

    def to_native(self, obj):

        ret     = super(SnippetRoFullSerializer, self).to_native(obj)
        #request = self.context.get('request')
        
        for k, v in ret.items():

            if not k.startswith('assigned_'): continue

            if not v:
                    
                del ret[k]
                continue

            #if 'assigned_intersect' in request.GET:

            #    uuids = request.GET.getlist(k)

            #    if not uuids:

            #        del ret[k]
            #        continue

            #    retrieves = []

            #    for uuid in uuids:

            #        # if uuid in v:
            #        # FIXME: Presence should be checked in the query
            #        # (works like this as long as uuid QSL request are 'AND').

            #            retrieves.append(reverse(self.assigned_retrieve[k],
            #                                     (uuid,), request=request))

            #    if retrieves: ret[k] = retrieves

            #    else: 

            #        del ret[k]
            #        continue

        return ret


class SnippetFilterView(ListAPIView):

    serializer_class = SnippetRoLightSerializer
    filter_class     = SnippetFilter
    model            = Snippet


# FIXME: not DRY at all, merge with MultipleLockedInput.
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

    # FIXME: at least one assigned object.
    def validate(self, attrs):

        # FIXME: move to view's pre_save()?
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
    serializer_class = SnippetRoFullSerializer
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
