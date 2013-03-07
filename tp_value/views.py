# -*- coding: utf-8 -*-
import django_filters

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from traceparent.mixins import RequestSerializerMixin

from tp_auth.views import UserRoLightSerializer

from .models import Unit, Quantity


class UnitFilter(django_filters.FilterSet):

    name    = django_filters.CharFilter(lookup_type='icontains')
    creator = django_filters.CharFilter(lookup_type='exact')

    class Meta:

        model = Unit
        fields = ('name', 'creator',)


class UnitSerializer(serializers.ModelSerializer):

    creator = UserRoLightSerializer()

    class Meta:

        model = Unit
        fields = ('uuid', 'creator', 'name', 'slug', 'symbol', 'decimal_places',)


class UnitCreateSerializer(RequestSerializerMixin, serializers.ModelSerializer):

    def validate(self, attrs):

        attrs['creator'] = self.request.user

        return attrs

    class Meta:

        model = Unit
        fields = ('uuid', 'name', 'slug', 'symbol', 'decimal_places',)


class UnitCreateView(CreateAPIView):

    def get(self, request, format=None): return Response(None)

    permission_classes = (IsAuthenticated,)
    serializer_class = UnitCreateSerializer
    model = Unit


class UnitFilterView(ListAPIView):

    serializer_class = UnitSerializer
    filter_class     = UnitFilter
    model            = Unit


#class QuantityFilter(django_filters.FilterSet):
#    creator__name= django_filters.CharFilter(lookup_type='creator__name__icontains')
##    max_price = django_filters.NumberFilter(lookup_type='lte')
#    class Meta:
#        model = Quantity
#        fields = ('name',)
##        fields = ['category', 'in_stock', 'min_price', 'max_price']


def t(a): print '>', a

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

    creator = UserRoLightSerializer()
    user    = UserRoLightSerializer()

#    previous = serializers.RelatedField(many=True)
#    previous = serializers.HyperlinkedRelatedField(many=True, read_only=False)

    class Meta:

        model = Quantity
        exclude = ('creator',)
        fields = ('unit', 'quantity', 'user', 'status', 'prev',)


class QuantityFilterView(ListAPIView):

    serializer_class = QuantitySerializer
    filter_class     = QuantityFilter
    model            = Quantity


class QuantityCreateView(CreateAPIView):

    def get(self, request, format=None): return Response(None)

    serializer_class   = QuantitySerializer
    model              = Quantity
    permission_classes = (IsAuthenticated,)
