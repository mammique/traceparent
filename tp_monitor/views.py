# -*- coding: utf-8 -*-
import django_filters

from rest_framework.generics import CreateAPIView, RetrieveAPIView, \
         RetrieveUpdateAPIView, ListAPIView
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
#from rest_framework import relations
from rest_framework.reverse import reverse
from rest_framework import status

from traceparent.mixins import DescActionMixin
from traceparent.fields import HyperlinkedFilterField
#from traceparent.widgets import MultipleLockedInput

#from tp_auth.permissions import IsCreatorOrUser

from .models import Counter


class CounterRoLightSerializer(serializers.ModelSerializer):

    url  = serializers.HyperlinkedIdentityField(view_name='tp_monitor_counter_retrieve') 
    user = serializers.HyperlinkedRelatedField(view_name='tp_auth_user_retrieve')

    class Meta:

        model  = Counter
        fields = ['uuid', 'url', 'user', 'datetime',]


class CounterRoFullSerializer(CounterRoLightSerializer):

    quantities = HyperlinkedFilterField(view_name='tp_value_quantity_filter',
                  lookup_params={'counters': 'pk'},
                  lookup_test=lambda o: o.quantities.all().count() != 0)

    assigned_metadata_snippets = \
        HyperlinkedFilterField(view_name='tp_metadata_snippet_filter',
                  lookup_params={'assigned_counters': 'pk'},
                  lookup_test=lambda o: o.assigned_metadata_snippets.all().count() != 0,
                  # querystring_params={'assigned_intersect': ''},
        )

    class Meta:

        model  = CounterRoLightSerializer.Meta.model
        fields = CounterRoLightSerializer.Meta.fields + \
                     ['quantities', 'datetime_start', 'datetime_stop',] + \
                     ['assigned_metadata_snippets',]
#                     ['quantities', 'datetime_start', 'datetime_stop', 'sums', 'graduations',]


class CounterFilter(django_filters.FilterSet):

    user       = django_filters.CharFilter(lookup_type='exact')
    quantities = django_filters.CharFilter(lookup_type='exact')
    
    # Metadata
    assigned_metadata_snippets = django_filters.CharFilter(lookup_type='exact')

    class Meta:

        model = Counter
        fields = ('user', 'quantities', 'assigned_metadata_snippets',)


class CounterFilterView(ListAPIView):

    serializer_class = CounterRoLightSerializer
    filter_class     = CounterFilter
    model            = Counter


class CounterRetrieveView(DescActionMixin, RetrieveAPIView):

    serializer_class    = CounterRoFullSerializer
    model               = Counter
    description_actions = (
    #                       ('Add graduation', lambda x: '%s?counters=%s' % \
    #                           (reverse('tp_monitor_graduation_create'), x.pk)),
                           ('Add metadata', lambda x: '%s?assigned_counters=%s' % \
                               (reverse('tp_metadata_snippet_create'), x.pk)),
    #                       ('Update', lambda x: reverse('tp_monitor_counter_update',
    #                           (x.pk,))),
                          )



class CounterAlterSerializer(serializers.ModelSerializer):
#class CounterAlterSerializer(CounterRoFullSerializer):#serializers.ModelSerializer):

    class Meta:

        model = Counter
        exclude = ('creator',)
        fields = ['user', 'datetime_start', 'datetime_stop',]


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

    #def create(self, request, *args, **kwargs):

    #    r = super(CounterCreateView, self).create(request, *args, **kwargs)

    #    if r.status_code == status.HTTP_201_CREATED:

    #        return Response(
    #                   CounterRoFullSerializer(
    #                       self.object,
    #                       context={
    #                           'request': self.request,
    #                           'format': self.format_kwarg,
    #                           'view': self}).data,
    #                   status=status.HTTP_201_CREATED)
    #        
    #    return r
