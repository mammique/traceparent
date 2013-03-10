# -*- coding: utf-8 -*-
import django_filters
from django.forms import widgets
from django.http import QueryDict

from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import relations
from rest_framework.reverse import reverse

#from tp_auth.views import UserRoLightSerializer

from .models import Unit, Quantity


class UnitFilter(django_filters.FilterSet):

    name    = django_filters.CharFilter(lookup_type='icontains')
    creator = django_filters.CharFilter(lookup_type='exact')

    class Meta:

        model = Unit
        fields = ('name', 'creator',)


#class UnitSerializer(serializers.HyperlinkedModelSerializer):#ModelSerializer):
class UnitSerializer(serializers.ModelSerializer):

    url     = serializers.HyperlinkedIdentityField(view_name='tp_value_unit_retrieve') 
    creator = serializers.HyperlinkedRelatedField(view_name='tp_auth_user_retrieve')

    class Meta:

        model = Unit
        fields = ('uuid', 'url', 'creator', 'name', 'slug', 'symbol', 'decimal_places',)


class UnitCreateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):

        attrs['creator'] = self.context['request'].user

        return attrs

    class Meta:

        model = Unit
        fields = ('uuid', 'name', 'slug', 'symbol', 'decimal_places',)


class UnitCreateView(CreateAPIView):

    def get(self, request, format=None): return Response(None)

    permission_classes = (IsAuthenticated,)
    serializer_class = UnitCreateSerializer
    model = Unit


class UnitRetrieveView(RetrieveAPIView):

    #def get(self, request, format=None): return Response(None)

    permission_classes = (IsAuthenticated,)
    serializer_class = UnitSerializer
    model = Unit


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


class HyperlinkedFilterField(serializers.Field):

    def __init__(self, *args, **kwargs):

        self.view_name     = kwargs.pop('view_name')
        self.format        = kwargs.pop('format', None)
        self.lookup_params = kwargs.pop('lookup_params')

        return super(HyperlinkedFilterField, self).__init__(*args, **kwargs)

    def field_to_native(self, o, *args, **kwargs):

        view_name = self.view_name
        request   = self.context.get('request', None)
        format    = self.format or self.context.get('format', None)

        query = QueryDict('', mutable=True)
        for key, field in self.lookup_params.items():
            query[key] = getattr(o, field)

        return '%s?%s' % (reverse(view_name, request=request, format=format),
                    query.urlencode())


class QuantitySerializer(serializers.ModelSerializer):

    url     = serializers.HyperlinkedIdentityField(view_name='tp_value_quantity_retrieve') 
    creator = serializers.HyperlinkedRelatedField(view_name='tp_auth_user_retrieve')
    user    = serializers.HyperlinkedRelatedField(view_name='tp_auth_user_retrieve')
    prev    = HyperlinkedFilterField(view_name='tp_value_quantity_filter',
                  lookup_params={'next': 'pk'})
    next    = HyperlinkedFilterField(view_name='tp_value_quantity_filter',
                  lookup_params={'prev': 'pk'})


    class Meta:

        model = Quantity
        #exclude = ('creator',)
        fields = ('uuid', 'unit', 'quantity', 'creator', 'user', \
            'status', 'datetime', 'prev', 'next',)


class QuantityFilterView(ListAPIView):

    serializer_class = QuantitySerializer
    filter_class     = QuantityFilter
    model            = Quantity


class QuantityCreateSerializer(serializers.ModelSerializer):

    prev = relations.PrimaryKeyRelatedField(required=False, # default='qsdfqsdfsqOOO',
               widget=widgets.TextInput(attrs={'disabled': True}))

    class Meta:

        model = Quantity
        exclude = ('creator',)
        fields = ('unit', 'quantity', 'user', 'prev', 'status',)


class QuantityCreateView(CreateAPIView):

    def get_serializer_context(self, *args, **kwargs):

        c    = super(QuantityCreateView, self).get_serializer_context(*args, **kwargs)
        prev = self.request.GET.get('prev')

        if prev: c.update({'form_initial': {'prev': prev}})

        return c

    def get(self, request, format=None): return Response(None)

    serializer_class   = QuantityCreateSerializer
    model              = Quantity
    permission_classes = (IsAuthenticated,)
