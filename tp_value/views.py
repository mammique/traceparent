# -*- coding: utf-8 -*-
import django_filters

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from traceparent.mixins import RequestSerializerMixin

from tp_auth.views import UserSerializer

from .models import Unit, Quantity


class UnitFilter(django_filters.FilterSet):

    uuid    = django_filters.CharFilter(lookup_type='exact')
    name    = django_filters.CharFilter(lookup_type='icontains')
    creator = django_filters.CharFilter(lookup_type='exact')

    class Meta:

        model = Unit
        fields = ('uuid', 'name', 'creator',)


class UnitSerializer(serializers.ModelSerializer):

    creator = UserSerializer()

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



class QuantitySerializer(serializers.ModelSerializer):

    creator = UserSerializer()
    user    = UserSerializer()

#    previous = serializers.RelatedField(many=True)
#    previous = serializers.HyperlinkedRelatedField(many=True, read_only=False)

    class Meta:

        model = Quantity
        exclude = ('creator',)
#        fields = ('album_name', 'artist', 'tracks')


class QuantityFilterView(ListAPIView):

    serializer_class = QuantitySerializer
    #filter_class     = QuantityFilter
    model            = Quantity


class QuantityCreateView(CreateAPIView):

    def get(self, request, format=None): return Response(None)

    serializer_class = QuantitySerializer
    model            = Quantity
