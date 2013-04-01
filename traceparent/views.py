# -*- coding: utf-8 -*-
from django.http import Http404

from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.fields import CharField
from rest_framework import status

from tp_auth.permissions import IsCreatorOrUser


class UUIDSerializer(serializers.Serializer):

    uuid    = CharField()
    objects = None

    def validate_uuid(self, attrs, source):

        uuid      = attrs[source]
        view      = self.context.get('view')
        m2m_field = getattr(view.object, view.m2m_field)
        model     = m2m_field.model

        if view.action == 'remove': q = m2m_field
        else: q = m2m_field.model.objects

        try: o = q.get(uuid=uuid)
        except model.DoesNotExist: raise Http404

        self.objects = [o]

        return attrs


class M2MAddRemoveView(RetrieveAPIView):

    action             = None
    m2m_field          = None
    serializer_class   = UUIDSerializer
    permission_classes = (IsAuthenticated, IsCreatorOrUser,)

    def get_name(self):

        if self.action: return self.action.title()

    def get(self, request, *args, **kwargs):

        super(M2MAddRemoveView, self).get(request, *args, **kwargs)

        return Response(None)

    def get_serializer(self, instance=None, data=None,
                       files=None, many=False, partial=False):

        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()

        return serializer_class(None, data=data, files=files,
                                many=many, partial=partial, context=context)

    def post(self, request, *args, **kwargs):

        self.m2m_field = kwargs.pop('m2m_field')
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        super(M2MAddRemoveView, self).get(request, *args, **kwargs)

        if serializer.is_valid():

            m2m_field = getattr(self.object, self.m2m_field)

            if self.action == 'remove': m2m_field.remove(*serializer.objects)
            else: m2m_field.add(*serializer.objects)

            self.object.save()#(update_fields=[self.m2m_field])

            return Response({'detail': 'OK'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class M2MAddView(M2MAddRemoveView):

    action = 'add'


class M2MRemoveView(M2MAddRemoveView):

    action = 'remove'
