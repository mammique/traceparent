# -*- coding: utf-8 -*-
from django.db import models

from django_extensions.db.fields import UUIDField

from traceparent.fields import SlugBlankToNoneField

from tp_auth.models import User
from tp_value.models import Unit, Quantity


visibility_choices = [
                      ('public',  u'public'),
                      ('private', u'private'),
                     ]

mimetype_choices   = [
                      ('text/plain', u'text/plain'),
                      ('application/json', u'application/json'),
                     ]


class Snippet(models.Model):

    uuid       = UUIDField(auto=True, primary_key=True)
    creator    = models.ForeignKey(User, related_name='metadata_snippets_created')
    user       = models.ForeignKey(User, related_name='metadata_snippets')
    visibility = models.SlugField(default='public', max_length=64,
                     choices=visibility_choices)
    mimetype   = models.SlugField(default='text/plain', max_length=64,
                     choices=mimetype_choices)
    slug       = models.SlugField(max_length=128)
    type       = SlugBlankToNoneField(max_length=64, null=True, blank=True, default=None)
    content    = models.TextField()
    datetime   = models.DateTimeField(auto_now_add=True)

    # Models
    assigned_users      = models.ManyToManyField(User, null=True, blank=True,
                              related_name='assigned_metadata_snippets')
    assigned_units      = models.ManyToManyField(Unit, null=True, blank=True,
                              related_name='assigned_metadata_snippets')
    assigned_quantities = models.ManyToManyField(Quantity, null=True, blank=True,
                              related_name='assigned_metadata_snippets')

    class Meta():

        ordering = ['-slug', '-datetime',]

    def __unicode__(self):
        return u'%s | %s | %s | %s <%s> %s' % \
            (self.slug, self.mimetype, self.type, self.visibility, self.pk, self.user)

