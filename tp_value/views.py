# -*- coding: utf-8 -*-
import django_filters
from django.forms import widgets
from django.http import QueryDict
from django.utils.safestring import mark_safe

from rest_framework.generics import CreateAPIView, UpdateAPIView, \
     RetrieveAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import relations
from rest_framework.reverse import reverse
from rest_framework import status

from traceparent.mixins import DescActionMixin

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


class QuantityRetrieveView(DescActionMixin, RetrieveAPIView):

    serializer_class    = QuantitySerializer
    model               = Quantity
    description_actions = (('Add next', lambda x: '%s?prev=%s' % \
                               (reverse('tp_value_quantity_create'), x.pk)),
                           ('Update', lambda x: reverse('tp_value_quantity_update',
                               (x.pk,))),
                          )


class QuantityFilterView(ListAPIView):

    serializer_class = QuantitySerializer
    filter_class     = QuantityFilter
    model            = Quantity


class QuantityPrevInput(widgets.MultipleHiddenInput):

    def render(self, name, value, attrs=None):

        r = super(QuantityPrevInput, self).render(name, value, attrs=None)

        if not value: return r

        q = Quantity.objects.get(pk=value[0])

        return mark_safe('%s<a href="%s" class="uneditable-input">%s</a>' % \
                   (r, reverse('tp_value_quantity_retrieve', (q.pk,)), q))


class QuantityAlterSerializer(serializers.ModelSerializer):
#class QuantityAlterSerializer(QuantitySerializer):#serializers.ModelSerializer):

    prev = relations.ManyPrimaryKeyRelatedField(required=False,
               widget=QuantityPrevInput)

    class Meta:

        model = Quantity
        exclude = ('creator',)
        fields = ('unit', 'quantity', 'user', 'prev', 'status',)

    def validate_status(self, attrs, source):

        if  attrs[source] == '': attrs[source] = None

        stat    = attrs[source]
        prev    = attrs['prev']
        request = self.context.get('request')

        if self.object and self.object.creator == request.user and \
               self.object.user != request.user and self.object.status in ('rejected',):

            raise serializers.ValidationError("""The creator of a quantity """ \
                      """cannot modify it if its status is set to 'rejected'.""")

        if stat != None and (not self.object or self.object.status == None):

            for q in prev:

                if not request.user in (q.creator, q.user,):

                    raise serializers.ValidationError("You cannot set a status as you """ \
                               """are not owner nor user of the previous quantity <%s>.""" % \
                                   q.pk)

        return attrs

    def validate(self, attrs):

        if not self.object: attrs['creator'] = self.context['request'].user

        return attrs


class QuantityCreateView(CreateAPIView):

    serializer_class   = QuantityAlterSerializer
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


#class QuantityUpdateView(DescActionMixin, RetrieveUpdateAPIView):
class QuantityUpdateView(DescActionMixin, RetrieveUpdateAPIView):

    serializer_class    = QuantityUpdateSerializer
    model               = Quantity
    permission_classes  = (IsAuthenticated, IsCreatorOrUser,)
    description_actions = (('Add next', lambda x: '%s?prev=%s' % \
                               (reverse('tp_value_quantity_create'), x.pk)),)

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
