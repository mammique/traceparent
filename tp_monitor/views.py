# -*- coding: utf-8 -*-
import django_filters

from django.shortcuts import get_object_or_404
from django.forms import widgets

from rest_framework.generics import CreateAPIView, RetrieveAPIView, \
         RetrieveUpdateAPIView, ListAPIView
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
#from rest_framework import relations
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework import relations

from traceparent.mixins import DescActionMixin
from traceparent.fields import HyperlinkedFilterField
from traceparent.widgets import MultipleLockedInput

from tp_auth.permissions import IsCreatorOrUser

from .models import Scope, Counter, ResultSum, Mark


class ScopeRoLightSerializer(serializers.ModelSerializer):

    url  = serializers.HyperlinkedIdentityField(view_name='tp_monitor_scope_retrieve')
    user = serializers.HyperlinkedRelatedField(view_name='tp_auth_user_retrieve')

    class Meta:

        model  = Scope
        fields = ['uuid', 'url', 'user', 'datetime',]


class ScopeRoFullSerializer(ScopeRoLightSerializer):

    counters   = HyperlinkedFilterField(view_name='tp_monitor_counter_filter',
                     lookup_params={'scopes': 'pk'},
                     lookup_test=lambda o: o.counters.all().count() != 0)

    quantities = HyperlinkedFilterField(view_name='tp_value_quantity_filter',
                     lookup_params={'scopes': 'pk'},
                     lookup_test=lambda o: o.quantities.all().count() != 0)

    assigned_metadata_snippets = \
        HyperlinkedFilterField(view_name='tp_metadata_snippet_filter',
            lookup_params={'assigned_scopes': 'pk'},
            lookup_test=lambda o: o.assigned_metadata_snippets.all().count() != 0,
            # querystring_params={'assigned_intersect': ''},
        )

    class Meta:

        model  = ScopeRoLightSerializer.Meta.model
        fields = ScopeRoLightSerializer.Meta.fields + \
                     ['counters', 'quantities', 'assigned_metadata_snippets',]


class ScopeFilter(django_filters.FilterSet):

    user       = django_filters.CharFilter(lookup_type='exact')
    counters   = django_filters.CharFilter(lookup_type='exact')
    quantities = django_filters.CharFilter(lookup_type='exact')
    
    # Metadata
    assigned_metadata_snippets = django_filters.CharFilter(lookup_type='exact')

    class Meta:

        model = Scope
        fields = ('user', 'counters', 'quantities', 'assigned_metadata_snippets',)


class ScopeFilterView(ListAPIView):

    serializer_class = ScopeRoLightSerializer
    filter_class     = ScopeFilter
    model            = Scope


class ScopeRetrieveView(DescActionMixin, RetrieveAPIView):

    serializer_class    = ScopeRoFullSerializer
    model               = Scope
    description_actions = (
                           ('Add new counter', lambda x: '%s?scopes=%s' % \
                               (reverse('tp_monitor_counter_create'), x.pk)),
                           ('Add new metadata', lambda x: '%s?assigned_scopes=%s' % \
                               (reverse('tp_metadata_snippet_create'), x.pk)),
                           ('Add/remove quantities', lambda x: \
                               (reverse('tp_monitor_scope_update_quantities', (x.pk,)))),
                          )


class ScopeAlterSerializer(serializers.ModelSerializer):
#class ScopeAlterSerializer(ScopeRoFullSerializer):#serializers.ModelSerializer):

    class Meta:

        model = Scope
        exclude = ('creator',)
        fields = ['user',]

    def validate(self, attrs):

        request = self.context.get('request')

        # FIXME: move to view's pre_save()?
        if not self.object: attrs['creator'] = request.user

        return attrs


class ScopeCreateView(CreateAPIView):

    serializer_class   = ScopeAlterSerializer
    model              = Scope
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None): return Response(None)

    def get_serializer_context(self, *args, **kwargs):

        c = super(ScopeCreateView, self).get_serializer_context(*args, **kwargs)

        # FIXME: not DRY at all, merge with MultipleLockedInput.        
        scope = self.request.GET.get('scopes')
        if scope:

            try:

                scope = Scope.objects.get(pk=scope)
                c.update({'form_initial': {'scopes': (scope.pk,)}})

            except self.model.DoesNotExist: pass

        return c

    def create(self, request, *args, **kwargs):

        r = super(ScopeCreateView, self).create(request, *args, **kwargs)

        if r.status_code == status.HTTP_201_CREATED:

            return Response(
                       ScopeRoFullSerializer(
                           self.object,
                           context={
                               'request': self.request,
                               'format': self.format_kwarg,
                               'view': self}).data,
                       status=status.HTTP_201_CREATED)
            
        return r


class CounterRoLightSerializer(serializers.ModelSerializer):

    url  = serializers.HyperlinkedIdentityField(view_name='tp_monitor_counter_retrieve') 
    user = serializers.HyperlinkedRelatedField(view_name='tp_auth_user_retrieve')

    class Meta:

        model  = Counter
        fields = ['uuid', 'url', 'user', 'datetime',]


class ResultSumSerializer(serializers.ModelSerializer):

    unit    = serializers.HyperlinkedRelatedField(view_name='tp_value_unit_retrieve')
    counter = serializers.HyperlinkedRelatedField(view_name='tp_monitor_counter_retrieve')

    class Meta:

        model  = ResultSum
        fields = ['unit', 'quantity', 'status', 'datetime', 'counter',] # TODO: remove counter on-the-fly if no present.


class CounterRoFullSerializer(CounterRoLightSerializer):

    scopes     = HyperlinkedFilterField(view_name='tp_monitor_scope_filter',
                     lookup_params={'counters': 'pk'},
                     lookup_test=lambda o: o.scopes.all().count() != 0)

    quantities = HyperlinkedFilterField(view_name='tp_value_quantity_filter',
                     lookup_params={'counters': 'pk'},
                     lookup_test=lambda o: o.quantities.all().count() != 0)

    marks      = HyperlinkedFilterField(view_name='tp_monitor_mark_filter',
                     lookup_params={'counters': 'pk'},
                     lookup_test=lambda o: o.marks.all().count() != 0)

    sums       = HyperlinkedFilterField(view_name='tp_monitor_result_sum_filter',
                     lookup_params={'counter': 'pk'},
                     lookup_test=lambda o: o.sums.all().count() != 0)

    # Metadata
    assigned_metadata_snippets = \
        HyperlinkedFilterField(view_name='tp_metadata_snippet_filter',
            lookup_params={'assigned_counters': 'pk'},
            lookup_test=lambda o: o.assigned_metadata_snippets.all().count() != 0,
            # querystring_params={'assigned_intersect': ''},
        )

    class Meta:

        model  = CounterRoLightSerializer.Meta.model
        fields = CounterRoLightSerializer.Meta.fields + \
                     ['scopes', 'quantities', 'sums', 'marks',
                      'datetime_start', 'datetime_stop',
                      'assigned_metadata_snippets',]


class CounterFilter(django_filters.FilterSet):

    user       = django_filters.CharFilter(lookup_type='exact')
    scopes     = django_filters.CharFilter(lookup_type='exact')
    quantities = django_filters.CharFilter(lookup_type='exact')
    marks      = django_filters.CharFilter(lookup_type='exact')
    
    # Metadata
    assigned_metadata_snippets = django_filters.CharFilter(lookup_type='exact')

    class Meta:

        model = Counter
        fields = ('user', 'scopes', 'quantities', 'marks', 'assigned_metadata_snippets',)


class CounterFilterView(ListAPIView):

    serializer_class = CounterRoLightSerializer
    filter_class     = CounterFilter
    model            = Counter


class CounterRetrieveView(DescActionMixin, RetrieveAPIView):

    serializer_class    = CounterRoFullSerializer
    model               = Counter
    description_actions = (
                           ('Add new mark', lambda x: '%s?counters=%s' % \
                               (reverse('tp_monitor_mark_create'), x.pk)),
                           ('Add new metadata', lambda x: '%s?assigned_counters=%s' % \
                               (reverse('tp_metadata_snippet_create'), x.pk)),
                           ('Update', lambda x: reverse('tp_monitor_counter_update',
                               (x.pk,))),
                          )



class CounterAlterSerializer(serializers.ModelSerializer):
#class CounterAlterSerializer(CounterRoFullSerializer):#serializers.ModelSerializer):

    scopes = relations.ManyPrimaryKeyRelatedField(required=False,
                 widget=MultipleLockedInput(
                            model=Scope,
                            view_name='tp_monitor_scope_retrieve'))

    class Meta:

        model   = Counter
        exclude = ('creator',)
        fields  = ['user', 'scopes', 'datetime_start', 'datetime_stop',]


    def validate(self, attrs):

        request = self.context.get('request')

        # FIXME: move to view's pre_save()?
        if not self.object: attrs['creator'] = request.user

        return attrs


class CounterCreateView(CreateAPIView):

    serializer_class   = CounterAlterSerializer
    model              = Counter
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None): return Response(None)

    def get_serializer_context(self, *args, **kwargs):

        c = super(CounterCreateView, self).get_serializer_context(*args, **kwargs)

        # FIXME: not DRY at all, merge with MultipleLockedInput.        
        scope = self.request.GET.get('scopes')
        if scope:

            try:

                scope = Scope.objects.get(pk=scope)
                c.update({'form_initial': {'scopes': (scope.pk,)}})

            except self.model.DoesNotExist: pass

        return c

    def create(self, request, *args, **kwargs):

        r = super(CounterCreateView, self).create(request, *args, **kwargs)

        if r.status_code == status.HTTP_201_CREATED:

            return Response(
                       CounterRoFullSerializer(
                           self.object,
                           context={
                               'request': self.request,
                               'format': self.format_kwarg,
                               'view': self}).data,
                       status=status.HTTP_201_CREATED)
            
        return r


class CounterUpdateSerializer(CounterAlterSerializer):

    class Meta:

        model            = Counter
        exclude          = ('creator',)
        fields           = ['scopes', 'datetime_start', 'datetime_stop',]
        read_only_fields = ('user',)


class CounterUpdateView(RetrieveUpdateAPIView):

    serializer_class   = CounterUpdateSerializer
    model              = Counter
    permission_classes = (IsAuthenticated, IsCreatorOrUser,)

    def get(self, request, format=None, *args, **kwargs):

        super(CounterUpdateView, self).get(request, format=None, *args, **kwargs)

        return Response({'FIXME':
            'https://github.com/tomchristie/django-rest-framework/issues/731'})

    def update(self, request, *args, **kwargs):

        r = super(CounterUpdateView, self).update(request, *args, **kwargs)

        if r.status_code == status.HTTP_200_OK:

            return Response(
                       CounterRoFullSerializer(
                           self.object,
                           context={
                               'request': self.request,
                               'format':  self.format_kwarg,
                               'view':    self}).data,
                       status=status.HTTP_200_OK)

        return r


class ResultSumFilter(django_filters.FilterSet):

    unit    = django_filters.CharFilter(lookup_type='exact')
    status  = django_filters.CharFilter(lookup_type='exact')
    counter = django_filters.CharFilter(lookup_type='exact')

    class Meta:

        model  = ResultSum
        fields = ('unit', 'status', 'counter',)


class ResultSumFilterView(ListAPIView):

    serializer_class = ResultSumSerializer
    filter_class     = ResultSumFilter
    model            = ResultSum


class MarkRoLightSerializer(serializers.ModelSerializer):

    url  = serializers.HyperlinkedIdentityField(view_name='tp_monitor_mark_retrieve') 
    user = serializers.HyperlinkedRelatedField(view_name='tp_auth_user_retrieve')
    unit = serializers.HyperlinkedRelatedField(view_name='tp_value_unit_retrieve')

    class Meta:

        model  = Mark
        fields = ['uuid', 'url', 'user', 'unit', 'quantity', 'statuses', 'datetime',]


class MarkRoFullSerializer(MarkRoLightSerializer):

    counters = HyperlinkedFilterField(view_name='tp_monitor_counter_filter',
                     lookup_params={'marks': 'pk'},
                     lookup_test=lambda o: o.counters.all().count() != 0)

    assigned_metadata_snippets = \
        HyperlinkedFilterField(view_name='tp_metadata_snippet_filter',
            lookup_params={'assigned_marks': 'pk'},
            lookup_test=lambda o: o.assigned_metadata_snippets.all().count() != 0,
            # querystring_params={'assigned_intersect': ''},
        )

    class Meta:

        model  = MarkRoLightSerializer.Meta.model
        fields = MarkRoLightSerializer.Meta.fields + \
                     ['counters', 'assigned_metadata_snippets',]


class MarkFilter(django_filters.FilterSet):

    user       = django_filters.CharFilter(lookup_type='exact')
    counters   = django_filters.CharFilter(lookup_type='exact')
    
    # Metadata
    assigned_metadata_snippets = django_filters.CharFilter(lookup_type='exact')

    class Meta:

        model = Mark
        fields = ('user', 'counters', 'assigned_metadata_snippets',)


class MarkFilterView(ListAPIView):

    serializer_class = MarkRoLightSerializer
    filter_class     = MarkFilter
    model            = Mark


class MarkRetrieveView(DescActionMixin, RetrieveAPIView):

    serializer_class    = MarkRoFullSerializer
    model               = Mark
    description_actions = (
                           ('Add new metadata', lambda x: '%s?assigned_marks=%s' % \
                               (reverse('tp_metadata_snippet_create'), x.pk)),
                           ('Update', lambda x: reverse('tp_monitor_mark_update',
                               (x.pk,))),
                          )


class MarkAlterSerializer(serializers.ModelSerializer):
#class MarkAlterSerializer(MarkRoFullSerializer):#serializers.ModelSerializer):

    counters = relations.ManyPrimaryKeyRelatedField(
                   widget=MultipleLockedInput(
                              model=Counter,
                              view_name='tp_monitor_counter_retrieve'))

    statuses = relations.ManyPrimaryKeyRelatedField(
                   widget=widgets.CheckboxSelectMultiple)

    class Meta:

        model   = Mark
        exclude = ('creator',)
        fields  = ['user', 'counters', 'unit', 'quantity', 'statuses',]

    def validate(self, attrs):

        request = self.context.get('request')

        # FIXME: move to view's pre_save()?
        if not self.object: attrs['creator'] = request.user

        return attrs


class MarkCreateView(CreateAPIView):

    serializer_class   = MarkAlterSerializer
    model              = Mark
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        return Response(None)

    def get_serializer_context(self, *args, **kwargs):

        c = super(MarkCreateView, self).get_serializer_context(*args, **kwargs)

        # FIXME: not DRY at all, merge with MultipleLockedInput.        
        counter = self.request.GET.get('counters')
        if counter:

            try:

                counter = Counter.objects.get(pk=counter)
                c.update({'form_initial': {'counters': (counter.pk,)}})

            except self.model.DoesNotExist: pass

        return c

    def create(self, request, *args, **kwargs):

        r = super(MarkCreateView, self).create(request, *args, **kwargs)

        if r.status_code == status.HTTP_201_CREATED:

            return Response(
                       MarkRoFullSerializer(
                           self.object,
                           context={
                               'request': self.request,
                               'format': self.format_kwarg,
                               'view': self}).data,
                       status=status.HTTP_201_CREATED)
            
        return r


class MarkUpdateSerializer(MarkAlterSerializer):

    class Meta:

        model            = Mark
        exclude          = ('creator',)
        fields           = ['counters', 'unit', 'quantity', 'statuses',]
        read_only_fields = ('user',)


class MarkUpdateView(RetrieveUpdateAPIView):

    serializer_class   = MarkUpdateSerializer
    model              = Mark
    permission_classes = (IsAuthenticated, IsCreatorOrUser,)

    def get(self, request, format=None, *args, **kwargs):

        super(MarkUpdateView, self).get(request, format=None, *args, **kwargs)

        return Response({'FIXME':
            'https://github.com/tomchristie/django-rest-framework/issues/731'})

    def update(self, request, *args, **kwargs):

        r = super(MarkUpdateView, self).update(request, *args, **kwargs)

        if r.status_code == status.HTTP_200_OK:

            return Response(
                       MarkRoFullSerializer(
                           self.object,
                           context={
                               'request': self.request,
                               'format':  self.format_kwarg,
                               'view':    self}).data,
                       status=status.HTTP_200_OK)

        return r
