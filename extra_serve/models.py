# -*- coding: utf-8 -*-
from django.db import models

from traceparent.models import UUIDModel

from tp_auth.models import User


class Bucket(models.Model):

    creator  = models.ForeignKey(User, related_name='serve_buckets_created')
    user     = models.ForeignKey(User, related_name='serve_buckets')
    slug     = models.SlugField(primary_key=True, max_length=32)
    users_ro = models.ManyToManyField(User, null=True, blank=True, related_name='serve_buckets_ro')
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta():

        ordering = ['-slug',]

    def __unicode__(self): return "%s %s" % (self.slug, self.user,)
