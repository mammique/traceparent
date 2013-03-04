# -*- coding: utf-8 -*-
#import django_filters

from rest_framework.generics import ListCreateAPIView
from rest_framework import serializers


from .models import Unit, Quantity


class UnitView(ListCreateAPIView):

#    serializer_class = UserSerializer
    model = Unit


#class QuantityFilter(django_filters.FilterSet):
#    creator__name= django_filters.CharFilter(lookup_type='creator__name__icontains')
##    max_price = django_filters.NumberFilter(lookup_type='lte')
#    class Meta:
#        model = Quantity
#        fields = ('name',)
##        fields = ['category', 'in_stock', 'min_price', 'max_price']



class QuantitySerializer(serializers.ModelSerializer):

#    previous = serializers.RelatedField(many=True)
#    previous = serializers.HyperlinkedRelatedField(many=True, read_only=False)

    class Meta:

        model = Quantity
#        fields = ('album_name', 'artist', 'tracks')

class QuantityView(ListCreateAPIView):

    serializer_class = QuantitySerializer
    model = Quantity
