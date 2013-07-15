# -*- coding: utf-8 -*-
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def client_headers_bounce(request):

    return Response(dict(filter(lambda x: x[0].startswith('HTTP_'), request.META.items())))
