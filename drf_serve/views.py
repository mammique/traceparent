# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponse

from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Bucket


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def bucket_file_nginx(request, user_pk, bucket_slug, filename):

    b = get_object_or_404(Bucket, slug=bucket_slug, user__pk=user_pk)

    if not request.user in (b.creator, b.user) and not \
        b.users_ro.filter(pk=request.user.pk).count(): raise PermissionDenied

    # http://djangosnippets.org/snippets/491/
    r = HttpResponse()
    del r['Content-Type']
    r['X-Accel-Redirect'] = '%(root)s/bucket/%(user_pk)s/%(bucket_slug)s/%(filename)s' % \
                               {'root': settings.DRF_SERVE_NGINX_INTERNAL_URL,
                                'user_pk': user_pk, 'bucket_slug': bucket_slug, 'filename': filename}
    return r

#class BucketFileRetrieveView(RetrieveAPIView):
#
    #model = Bucket

    #def retrieve(self, request, user_pk, bucket_slug, filename, *args, **kwargs):
#
        #self.object = self.get_object()
        #serializer = self.get_serializer(self.object)
        #return Response(serializer.data)

    #def get(self, request, user_pk, bucket_slug, filename, *args, **kwargs):

        

    #def get(self, request, serve_content=False, *args, **kwargs):
#
        #r = super(BucketFileRetrieveView, self).get(request, *args, **kwargs)
#
        #if not serve_content: return r
#
        #r = HttpResponse(self.object.content, content_type=self.object.mimetype)
#
        #if 'download' in request.GET:
            #r['Content-Disposition'] = u"attachment; filename*=UTF-8''%s." % \
                                           #urllib.quote(self.object.slug)
#
        #return r
