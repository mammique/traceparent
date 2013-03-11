# -*- coding: utf-8 -*-
import django_filters
from django.forms import widgets
from django.http import QueryDict
from django.utils.safestring import mark_safe

from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import relations
from rest_framework.reverse import reverse
from rest_framework import status

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
        self.lookup_test   = kwargs.pop('lookup_test', None)

        return super(HyperlinkedFilterField, self).__init__(*args, **kwargs)

    def field_to_native(self, o, *args, **kwargs):

        if self.lookup_test and not self.lookup_test(o): return None

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


class QuantityDescMixin(object):

    def get_description(self, *args, **kwargs):

        desc = super(QuantityDescMixin, self).get_description(*args, **kwargs)

        if kwargs['html']:
            
            desc += """<div class="btn-group">""" \
                    """<a class="btn btn-primary dropdown-toggle" """ \
                    """data-toggle="dropdown" href="#">""" \
                    """Action <span class="caret"></span></a><ul class="dropdown-menu">""" \
                    """<li><a href="%s?prev=%s">Add next</a></li></ul></div>""" % \
                        (reverse('tp_value_quantity_create'), self.object.pk)
            desc = mark_safe(desc)

        return desc


class QuantityRetrieveView(QuantityDescMixin, RetrieveAPIView):

    serializer_class   = QuantitySerializer
    model              = Quantity


class QuantityFilterView(ListAPIView):

    serializer_class = QuantitySerializer
    filter_class     = QuantityFilter
    model            = Quantity


class QuantityPrevInput(widgets.MultipleHiddenInput):

    #def __init__(self, *args, **kwargs):

    #    return super(QuantityPrevInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):

        r = super(QuantityPrevInput, self).render(name, value, attrs=None)

        if not value: return r

        q = Quantity.objects.get(pk=value[0])

        return mark_safe('%s<a href="%s" class="uneditable-input">%s</a>' % \
                   (r, reverse('tp_value_quantity_retrieve', (q.pk,)), q))


class QuantityCreateSerializer(serializers.ModelSerializer):

    prev = relations.ManyPrimaryKeyRelatedField(required=False,
               widget=QuantityPrevInput)

    class Meta:

        model = Quantity
        exclude = ('creator',)
        fields = ('unit', 'quantity', 'user', 'prev', 'status',)

    def validate_status(self, attrs, source):

        if attrs[source] == '': attrs[source] = None

        return attrs

    def validate(self, attrs):

        attrs['creator'] = self.context['request'].user

        return attrs


class QuantityCreateView(QuantityDescMixin, CreateAPIView):

    serializer_class   = QuantityCreateSerializer
    model              = Quantity
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self, *args, **kwargs):

        c    = super(QuantityCreateView, self).get_serializer_context(*args, **kwargs)
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

            o = self.object
            return Response(QuantitySerializer(o).data, status=status.HTTP_201_CREATED) # FIXME: request!
            
        return r
