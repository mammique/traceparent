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
#from tp_auth.views import UserRoLightSerializer

from .models import Unit, Quantity


class UnitFilter(django_filters.FilterSet):

    name    = django_filters.CharFilter(lookup_type='icontains')
    creator = django_filters.CharFilter(lookup_type='exact')

    class Meta:

        model = Unit
        fields = ('name', 'creator',)


class UnitSerializer(serializers.ModelSerializer):

    url     = serializers.HyperlinkedIdentityField(view_name='tp_value_unit_retrieve') 
    creator = serializers.HyperlinkedRelatedField(view_name='tp_auth_user_retrieve')

    class Meta:

        model = Unit
        fields = ('uuid', 'url', 'creator', 'name', 'slug', 'symbol', 'decimal_places',)


class UnitCreateSerializer(serializers.ModelSerializer):

    class Meta:

        model = Unit
        fields = ('uuid', 'name', 'slug', 'symbol', 'decimal_places',)

    def validate(self, attrs):

        attrs['creator'] = self.context['request'].user

        return attrs


class UnitCreateView(CreateAPIView):

    def get(self, request, format=None): return Response(None)

    permission_classes = (IsAuthenticated,)
    serializer_class = UnitCreateSerializer
    model = Unit


class UnitRetrieveView(DescActionMixin, RetrieveAPIView):

    #def get(self, request, format=None): return Response(None)

    permission_classes = (IsAuthenticated,)
    serializer_class = UnitSerializer
    model = Unit
    description_actions = (('Add metadata', lambda x: '%s?assigned_units=%s' % \
                               (reverse('tp_metadata_snippet_create'), x.pk)),)


class UnitFilterView(ListAPIView):

    serializer_class = UnitSerializer
    filter_class     = UnitFilter
    model            = Unit


class QuantityFilter(django_filters.FilterSet):

    name     = django_filters.CharFilter(lookup_type='icontains')
    user     = django_filters.CharFilter(lookup_type='exact')
    unit     = django_filters.CharFilter(lookup_type='exact')
#    creator  = django_filters.CharFilter(lookup_type='exact')
    prev     = django_filters.CharFilter(lookup_type='exact')
    next     = django_filters.CharFilter(lookup_type='exact')

    class Meta:

        model = Quantity
        fields = ('name', 'user', 'unit', 'prev', 'next',)


class QuantitySerializer(serializers.ModelSerializer):

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

    class Meta:

        model = Quantity
        exclude = ('creator',)
        fields = ('uuid', 'url', 'unit', 'quantity', 'creator', 'user', \
            'status', 'datetime', 'prev', 'next',)


class QuantityRetrieveView(DescActionMixin, RetrieveAPIView):

    serializer_class    = QuantitySerializer
    model               = Quantity
    description_actions = (('Add next', lambda x: '%s?prev=%s' % \
                               (reverse('tp_value_quantity_create'), x.pk)),
                           ('Add metadata', lambda x: '%s?assigned_quantities=%s' % \
                               (reverse('tp_metadata_snippet_create'), x.pk)),
                           ('Update', lambda x: reverse('tp_value_quantity_update',
                               (x.pk,))),
                          )


class QuantityFilterView(ListAPIView):

    serializer_class = QuantitySerializer
    filter_class     = QuantityFilter
    model            = Quantity


class QuantityAlterSerializer(serializers.ModelSerializer):
#class QuantityAlterSerializer(QuantitySerializer):#serializers.ModelSerializer):

    prev = relations.ManyPrimaryKeyRelatedField(required=False,
               widget=MultipleLockedInput(model=Quantity))

    class Meta:

        model = Quantity
        exclude = ('creator',)
        fields = ('unit', 'quantity', 'user', 'prev', 'status',)

    def validate_status(self, attrs, source):

        if  attrs[source] == '': attrs[source] = None

        stat    = attrs[source]
        prev    = attrs['prev']
        request = self.context.get('request')

        # FIXME: forbid non-null statuses to become null?
        if stat != None and (not self.object or self.object.status == None):

            for q in prev:

                # FIXME: call `IsCreatorOrUser` instead?
                if not request.user in (q.creator, q.user,):

                    raise serializers.ValidationError("You cannot set a status as you """ \
                               """are not owner nor user of the previous quantity <%s>.""" % \
                                   q.pk)

        return attrs

    def validate(self, attrs):

        request = self.context.get('request')

        if not self.object: attrs['creator'] = self.context['request'].user

        # FIXME: move this to the permission level?
        elif self.object.creator == request.user and \
               self.object.user != request.user and self.object.status in ('rejected',):

            raise serializers.ValidationError("""The creator of a quantity """ \
                      """cannot modify it if its status is set to 'rejected'.""")

        return attrs


class QuantityCreateView(CreateAPIView):

    serializer_class   = QuantityAlterSerializer
    model              = Quantity
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self, *args, **kwargs):

        c    = super(QuantityCreateView, self).get_serializer_context(*args, **kwargs)

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
                       QuantitySerializer(
                           self.object,
                           context={
                               'request': self.request,
                               'format': self.format_kwarg,
                               'view': self}).data,
                       status=status.HTTP_201_CREATED)
            
        return r


class QuantityUpdateSerializer(QuantityAlterSerializer):

    class Meta:

        model = Quantity
        exclude = ('creator',)
        fields = ('unit', 'quantity', 'prev', 'status',)
        read_only_fields = ('user',)


class QuantityUpdateView(RetrieveUpdateAPIView):
# class QuantityUpdateView(DescActionMixin, RetrieveUpdateAPIView):

    serializer_class    = QuantityUpdateSerializer
    model               = Quantity
    permission_classes  = (IsAuthenticated, IsCreatorOrUser,)
    #description_actions = (('Add next', lambda x: '%s?prev=%s' % \
    #                           (reverse('tp_value_quantity_create'), x.pk)),
    #                       ('Add metadata', lambda x: '%s?assigned_quantities=%s' % \
    #                           (reverse('tp_metadata_snippet_create'), x.pk)),
    #                       )

    def get(self, request, format=None, *args, **kwargs):

        super(QuantityUpdateView, self).get(request, format=None, *args, **kwargs)

        return Response({'FIXME':
            'https://github.com/tomchristie/django-rest-framework/issues/731'})

    def update(self, request, *args, **kwargs):

        r = super(QuantityUpdateView, self).update(request, *args, **kwargs)

        if r.status_code == status.HTTP_200_OK:

            return Response(
                       QuantitySerializer(
                           self.object,
                           context={
                               'request': self.request,
                               'format': self.format_kwarg,
                               'view': self}).data,
                       status=status.HTTP_200_OK)

        return r

    
    #def get_serializer(self, *args, **kwargs):

    #    print args, kwargs
    #    return super(QuantityUpdateView, self).get_serializer(*args, **kwargs)
