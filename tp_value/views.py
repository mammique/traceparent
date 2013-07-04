# -*- coding: utf-8 -*-
import django_filters

from rest_framework.generics import CreateAPIView, RetrieveAPIView, \
         RetrieveUpdateAPIView, ListAPIView
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import relations
from rest_framework.reverse import reverse
from rest_framework import status

from traceparent.mixins import DescActionMixin
from traceparent.fields import HyperlinkedFilterField
from traceparent.widgets import MultipleLockedInput

from tp_auth.permissions import IsCreatorOrUser

from .models import Unit, Quantity


class UnitFilter(django_filters.FilterSet):

    name    = django_filters.CharFilter(lookup_type='icontains')
    creator = django_filters.CharFilter(lookup_type='exact')
    slug    = django_filters.CharFilter(lookup_type='icontains')

    class Meta:

        model = Unit
        fields = ('name', 'creator',)


class UnitRoLightSerializer(serializers.ModelSerializer):

    url     = serializers.HyperlinkedIdentityField(view_name='tp_value_unit_retrieve') 
    creator = serializers.HyperlinkedRelatedField(view_name='tp_auth_user_retrieve')

    class Meta:

        model  = Unit
        fields = ['uuid', 'url', 'creator', 'name', 'slug', 'symbol', 'decimal_places',]


class UnitRoFullSerializer(UnitRoLightSerializer):

    assigned_metadata_snippets = \
        HyperlinkedFilterField(view_name='tp_metadata_snippet_filter',
                  lookup_params={'assigned_units': 'pk'},
                  lookup_test=lambda o: o.assigned_metadata_snippets.all().count() != 0,
                  # querystring_params={'assigned_intersect': ''},
        )

    class Meta:

        model  = UnitRoLightSerializer.Meta.model
        fields = UnitRoLightSerializer.Meta.fields + ['assigned_metadata_snippets',]


class UnitCreateSerializer(serializers.ModelSerializer):

    class Meta:

        model  = Unit
        fields = ('uuid', 'name', 'slug', 'symbol', 'decimal_places',)

    def validate(self, attrs):

        # FIXME: move to view's pre_save()?
        attrs['creator'] = self.context['request'].user

        return attrs


class UnitCreateView(CreateAPIView):

    def get(self, request, format=None): return Response(None)

    permission_classes = (IsAuthenticated,)
    serializer_class   = UnitCreateSerializer
    model              = Unit


class UnitRetrieveView(DescActionMixin, RetrieveAPIView):

    #def get(self, request, format=None): return Response(None)

    #permission_classes  = (IsAuthenticated,)
    serializer_class    = UnitRoFullSerializer
    model               = Unit
    description_actions = (('Add new metadata', lambda x: '%s?assigned_units=%s' % \
                               (reverse('tp_metadata_snippet_create'), x.pk)),)


class UnitFilterView(ListAPIView):

    serializer_class = UnitRoLightSerializer
    filter_class     = UnitFilter
    model            = Unit


class QuantityFilter(django_filters.FilterSet):

    # TODO: exclude null statuses by default?
    # https://django-filter.readthedocs.org/en/latest/ref/filters.html#action
    user     = django_filters.CharFilter(lookup_type='exact')
    unit     = django_filters.CharFilter(lookup_type='exact')
#    creator  = django_filters.CharFilter(lookup_type='exact')
    prev     = django_filters.CharFilter(lookup_type='exact')
    next     = django_filters.CharFilter(lookup_type='exact')
    status   = django_filters.CharFilter(lookup_type='exact')
 
    # Metadata
    assigned_metadata_snippets = django_filters.CharFilter(lookup_type='exact')

    # Monitor
    scopes   = django_filters.CharFilter(lookup_type='exact')
    counters = django_filters.CharFilter(lookup_type='exact')

    class Meta:

        model  = Quantity
        fields = ('creator', 'user', 'unit', 'prev', 'next', 'status', # FIXME: allow creator for other models too?
                  'assigned_metadata_snippets', 'scopes', 'counters',)


class QuantityRoLightSerializer(serializers.ModelSerializer):

    url     = serializers.HyperlinkedIdentityField(view_name='tp_value_quantity_retrieve') 
    creator = serializers.HyperlinkedRelatedField(view_name='tp_auth_user_retrieve')
    user    = serializers.HyperlinkedRelatedField(view_name='tp_auth_user_retrieve')
    unit    = serializers.HyperlinkedRelatedField(view_name='tp_value_unit_retrieve')
    prev    = HyperlinkedFilterField(view_name='tp_value_quantity_filter',
                  lookup_params={'next': 'pk'},
                  lookup_test=lambda o: o.prev.all().count() != 0)
    next    = HyperlinkedFilterField(view_name='tp_value_quantity_filter',
                  lookup_params={'prev': 'pk'},
                  lookup_test=lambda o: o.next.all().count() != 0)

    def to_native(self, obj):

        ret     = super(QuantityRoLightSerializer, self).to_native(obj)
        request = self.context.get('request')

        if obj.user_visibility == 'public': return ret

        elif obj.user_visibility == 'private':

            if not request.user.is_authenticated() or not \
                request.user in (obj.creator, obj.user,): del ret['user']

            return ret

    class Meta:

        model   = Quantity
        exclude = ('creator',)
        fields  = ['uuid', 'url', 'unit', 'quantity', 'creator', 'user', \
                   'status', 'datetime', 'prev', 'next',]


class QuantityRoFullSerializer(QuantityRoLightSerializer):

    assigned_metadata_snippets = \
        HyperlinkedFilterField(view_name='tp_metadata_snippet_filter',
                  lookup_params={'assigned_quantities': 'pk'},
                  lookup_test=lambda o: o.assigned_metadata_snippets.all().count() != 0,
                  # querystring_params={'assigned_intersect': ''},
    )

    scopes = HyperlinkedFilterField(view_name='tp_monitor_scope_filter',
                  lookup_params={'quantities': 'pk'},
                  lookup_test=lambda o: o.scopes.all().count() != 0,
                  # querystring_params={'assigned_intersect': ''},
    )

    counters = HyperlinkedFilterField(view_name='tp_monitor_counter_filter',
                  lookup_params={'quantities': 'pk'},
                  lookup_test=lambda o: o.counters.all().count() != 0,
                  # querystring_params={'assigned_intersect': ''},
    )


    class Meta:

        model   = QuantityRoLightSerializer.Meta.model
        exclude = QuantityRoLightSerializer.Meta.exclude
        fields  = QuantityRoLightSerializer.Meta.fields + \
                      ['assigned_metadata_snippets', 'scopes', 'counters',]


class QuantityRetrieveView(DescActionMixin, RetrieveAPIView):

    serializer_class    = QuantityRoFullSerializer
    model               = Quantity
    description_actions = (
                           ('Add new next', lambda x: '%s?prev=%s' % \
                               (reverse('tp_value_quantity_create'), x.pk)),
                           ('Add new metadata', lambda x: '%s?assigned_quantities=%s' % \
                               (reverse('tp_metadata_snippet_create'), x.pk)),
                           ('Update', lambda x: reverse('tp_value_quantity_update',
                               (x.pk,))),
                          )


# TODO: prevent private quantities from being fetched by anonymous or other users.
class QuantityFilterView(ListAPIView):

    serializer_class = QuantityRoLightSerializer
    filter_class     = QuantityFilter
    model            = Quantity


class QuantityAlterSerializer(serializers.ModelSerializer):
#class QuantityAlterSerializer(QuantityRoFullSerializer):#serializers.ModelSerializer):

    prev = relations.ManyPrimaryKeyRelatedField(required=False,
               widget=MultipleLockedInput(
                          model=Quantity,
                          view_name='tp_value_quantity_retrieve'))

    class Meta:

        model   = Quantity
        exclude = ('creator',)
        fields  = ('unit', 'quantity', 'user', 'user_visibility', 'prev', 'status',)

    def validate_status(self, attrs, source):

        stat = attrs[source]

        if not 'prev' in attrs: prev = self.object.prev.all() # Update
        else : prev = attrs['prev']                           # Create

        request = self.context.get('request')

        # FIXME: forbid non-symbolic statuses to become symbolic?
        if stat.slug != 'symbolic' and \
            (not self.object or self.object.status.slug == 'symbolic'):

            for q in prev:

                # FIXME: call `IsCreatorOrUser` instead?
                if not request.user in (q.creator, q.user,):

                    raise serializers.ValidationError("You cannot define a non-symbolic status as you """ \
                               """are not the owner nor user of the previous quantity <%s>.""" % \
                                   q.pk)

        return attrs

    def validate(self, attrs):

        request = self.context.get('request')

        # FIXME: move to view's pre_save()?
        if not self.object: attrs['creator'] = request.user

        # FIXME: move this to the permission level?
        elif self.object.creator == request.user and \
            self.object.user != request.user and self.object.status.slug in ('rejected',):

            raise serializers.ValidationError("""The creator of a quantity """ \
                      """cannot modify it if its status is set to 'rejected'.""")

        return attrs


class QuantityCreateView(CreateAPIView):

    serializer_class   = QuantityAlterSerializer
    model              = Quantity
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self, *args, **kwargs):

        c = super(QuantityCreateView, self).get_serializer_context(*args, **kwargs)

        # FIXME: not DRY at all, merge with MultipleLockedInput.        
        prev = self.request.GET.get('prev')
        if prev:

            try:

                prev = self.model.objects.get(pk=prev)
                c.update({'form_initial': {'prev': (prev.pk,), 'unit': prev.unit.pk}})

            except self.model.DoesNotExist: pass

        return c

    def get(self, request, format=None): return Response(None)

    def create(self, request, *args, **kwargs):

        r = super(QuantityCreateView, self).create(request, *args, **kwargs)

        if r.status_code == status.HTTP_201_CREATED:

            return Response(
                       QuantityRoFullSerializer(
                           self.object,
                           context={
                               'request': self.request,
                               'format':  self.format_kwarg,
                               'view':    self}).data,
                       status=status.HTTP_201_CREATED)
            
        return r


class QuantityUpdateSerializer(QuantityAlterSerializer):

    class Meta:

        model            = Quantity
        exclude          = ('creator',)
#        fields           = ('unit', 'user_visibility', 'quantity', 'prev', 'status',)
        fields           = ('user_visibility', 'status', 'prev',)
        read_only_fields = ('user', 'unit', 'quantity',)


class QuantityUpdateView(RetrieveUpdateAPIView):

    serializer_class   = QuantityUpdateSerializer
    model              = Quantity
    permission_classes = (IsAuthenticated, IsCreatorOrUser,)

    def get(self, request, format=None, *args, **kwargs):

        super(QuantityUpdateView, self).get(request, format=None, *args, **kwargs)

        return Response({'FIXME':
            'https://github.com/tomchristie/django-rest-framework/issues/731'})

    def update(self, request, *args, **kwargs):

        r = super(QuantityUpdateView, self).update(request, *args, **kwargs)

        if r.status_code == status.HTTP_200_OK:

            return Response(
                       QuantityRoFullSerializer(
                           self.object,
                           context={
                               'request': self.request,
                               'format':  self.format_kwarg,
                               'view':    self}).data,
                       status=status.HTTP_200_OK)

        return r
