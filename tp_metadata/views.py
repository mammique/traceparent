# -*- coding: utf-8 -*-
import django_filters, urllib

from django.http import HttpResponse
from django.forms import widgets
from django.db.models import Q

from rest_framework.generics import ListAPIView, CreateAPIView, \
        RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import relations
from rest_framework.reverse import reverse
from rest_framework import status

from traceparent.fields import HyperlinkedFilterField
from traceparent.widgets import MultipleLockedInput
from traceparent.mixins import DescActionMixin

from tp_auth.permissions import IsCreatorOrUser # ObjectIsPublic

from .models import Snippet


class SnippetRoMixin(object):

    def get_queryset(self):

        queryset = super(SnippetRoMixin, self).get_queryset()
        public   = queryset.filter(visibility='public')

        # FIXME: non-auth users will get a 404 instead of 401 or 403.
        if self.request.user.is_authenticated():

            queryset = public | \
                queryset.filter(Q(creator=self.request.user) | Q(user=self.request.user))

        else: queryset = public

        return queryset


class SnippetFilter(django_filters.FilterSet):

    creator  = django_filters.CharFilter(lookup_type='exact')
    user     = django_filters.CharFilter(lookup_type='exact')
    mimetype = django_filters.CharFilter(lookup_type='exact')
    slug     = django_filters.CharFilter(lookup_type=None)
    type     = django_filters.CharFilter(lookup_type='iexact')

    # Models
    assigned_users      = django_filters.CharFilter(lookup_type='exact')
    assigned_units      = django_filters.CharFilter(lookup_type='exact')
    assigned_quantities = django_filters.CharFilter(lookup_type='exact')
    #assigned_quantities = django_filters.ModelMultipleChoiceFilter()
    assigned_scopess    = django_filters.CharFilter(lookup_type='exact')
    assigned_counters   = django_filters.CharFilter(lookup_type='exact')
    assigned_marks      = django_filters.CharFilter(lookup_type='exact')


    class Meta:

        model = Snippet
        fields = ('creator', 'user', 'mimetype', 'slug', 'type',
                  'assigned_users', 'assigned_units',
                  'assigned_quantities', 'assigned_scopes',
                  'assigned_counters', 'assigned_marks',)


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
    assigned_scopes = HyperlinkedFilterField(view_name='tp_monitor_scope_filter',
                  lookup_params={'assigned_metadata_snippets': 'pk'},
                  lookup_test=lambda o: o.assigned_scopes.all().count() != 0)
    assigned_counters = HyperlinkedFilterField(view_name='tp_monitor_counter_filter',
                  lookup_params={'assigned_metadata_snippets': 'pk'},
                  lookup_test=lambda o: o.assigned_counters.all().count() != 0)
    assigned_marks = HyperlinkedFilterField(view_name='tp_monitor_mark_filter',
                  lookup_params={'assigned_metadata_snippets': 'pk'},
                  lookup_test=lambda o: o.assigned_marks.all().count() != 0)



    #assigned_retrieve = {
    #                     'assigned_users': 'tp_auth_user_retrieve',
    #                     'assigned_units': 'tp_value_unit_retrieve',
    #                     'assigned_quantities': 'tp_value_quantity_retrieve',
    #                    }

    class Meta:

        model  = SnippetRoLightSerializer.Meta.model
        fields = SnippetRoLightSerializer.Meta.fields + \
                     ['assigned_users', 'assigned_units', 'assigned_quantities',
                      'assigned_scopes', 'assigned_counters', 'assigned_marks']

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


class SnippetFilterView(SnippetRoMixin, ListAPIView):

    serializer_class = SnippetRoLightSerializer
    filter_class     = SnippetFilter
    model            = Snippet


# FIXME: not DRY at all, merge with MultipleLockedInput.
from tp_value.models import Unit, Quantity
from tp_auth.models import User
from tp_monitor.models import Scope, Counter, Mark

class SnippetAlterSerializer(serializers.ModelSerializer):

    content             = CharField(widget=widgets.Textarea)
    assigned_users      = relations.ManyPrimaryKeyRelatedField(required=False,
                              widget=MultipleLockedInput(
                                         model=User,
                                         view_name='tp_auth_user_retrieve'))
    assigned_units      = relations.ManyPrimaryKeyRelatedField(required=False,
                              widget=MultipleLockedInput(
                                         model=Unit,
                                         view_name='tp_value_unit_retrieve'))
    assigned_quantities = relations.ManyPrimaryKeyRelatedField(required=False,
                              widget=MultipleLockedInput(
                                         model=Quantity,
                                         view_name='tp_value_quantity_retrieve'))
    assigned_scopes     = relations.ManyPrimaryKeyRelatedField(required=False,
                              widget=MultipleLockedInput(
                                         model=Scope,
                                         view_name='tp_monitor_scope_retrieve'))
    assigned_counters   = relations.ManyPrimaryKeyRelatedField(required=False,
                              widget=MultipleLockedInput(
                                         model=Counter,
                                         view_name='tp_monitor_counter_retrieve'))
    assigned_marks      = relations.ManyPrimaryKeyRelatedField(required=False,
                              widget=MultipleLockedInput(
                                         model=Mark,
                                         view_name='tp_monitor_mark_retrieve'))

    class Meta:

        model  = Snippet
        fields = ['visibility', 'mimetype', 'slug', 'type', 'content',
                  'assigned_users', 'assigned_units',
                  'assigned_quantities',
                  'assigned_scopes', 'assigned_counters', 'assigned_marks',]


class SnippetCreateSerializer(SnippetAlterSerializer):

    class Meta:

        model  = SnippetAlterSerializer.Meta.model
        fields = ['user',] + SnippetAlterSerializer.Meta.fields

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

        # FIXME: not DRY at all, merge with MultipleLockedInput.
        assigned_scope = self.request.GET.get('assigned_scopes')
        if assigned_scope:

            try:

                assigned_scope = Scope.objects.get(pk=assigned_scope)
                form_initial.update({'assigned_scopes': (assigned_scope.pk,),})

            except Scope.DoesNotExist: pass

        # FIXME: not DRY at all, merge with MultipleLockedInput.
        assigned_counter = self.request.GET.get('assigned_counters')
        if assigned_counter:

            try:

                assigned_counter = Counter.objects.get(pk=assigned_counter)
                form_initial.update({'assigned_counters': (assigned_counter.pk,),})

            except Counter.DoesNotExist: pass

        # FIXME: not DRY at all, merge with MultipleLockedInput.
        assigned_mark = self.request.GET.get('assigned_marks')
        if assigned_mark:

            try:

                assigned_mark = Mark.objects.get(pk=assigned_mark)
                form_initial.update({'assigned_marks': (assigned_mark.pk,),})

            except Mark.DoesNotExist: pass

        c = super(SnippetCreateView, self).get_serializer_context(*args, **kwargs)
        c.update({'form_initial': form_initial})

        return c

    def create(self, request, *args, **kwargs):

        r = super(SnippetCreateView, self).create(request, *args, **kwargs)

        if r.status_code == status.HTTP_201_CREATED:

            return Response(
                       SnippetRoFullSerializer(
                           self.object,
                           context={
                               'request': self.request,
                               'format': self.format_kwarg,
                               'view': self}).data,
                       status=status.HTTP_201_CREATED)
            
        return r


class SnippetUpdateView(RetrieveUpdateDestroyAPIView):

    permission_classes = (IsAuthenticated, IsCreatorOrUser,)
    model              = Snippet
    serializer_class   = SnippetAlterSerializer

    def get(self, request, format=None, *args, **kwargs):

        super(SnippetUpdateView, self).get(request, format=None, *args, **kwargs)

        return Response({'FIXME':
            'https://github.com/tomchristie/django-rest-framework/issues/731'})

    def update(self, request, *args, **kwargs):

        r = super(SnippetUpdateView, self).update(request, *args, **kwargs)

        if r.status_code == status.HTTP_200_OK:

            return Response(
                       SnippetRoFullSerializer(
                           self.object,
                           context={
                               'request': self.request,
                               'format': self.format_kwarg,
                               'view': self}).data,
                       status=status.HTTP_200_OK)

        return r


class SnippetRetrieveView(DescActionMixin, SnippetRoMixin, RetrieveAPIView):

    model               = Snippet
    serializer_class    = SnippetRoFullSerializer
    description_actions = (('Update', lambda x: reverse('tp_metadata_snippet_update',
                                (x.pk,))),)

    def get(self, request, serve_content=False, *args, **kwargs):

        r = super(SnippetRetrieveView, self).get(request, *args, **kwargs)

        if not serve_content: return r

        r = HttpResponse(self.object.content, content_type=self.object.mimetype)

        if 'download' in request.GET:
            r['Content-Disposition'] = u"attachment; filename*=UTF-8''%s." % \
                                           urllib.quote(self.object.slug)

        return r
