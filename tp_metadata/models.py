# -*- coding: utf-8 -*-
from django.db import models

from traceparent.fields import SlugBlankToNoneField
from traceparent.models import UUIDModel

from tp_auth.models import User
from tp_auth import VISIBILITY_CHOICES
from tp_value.models import Unit, Quantity
from tp_monitor.models import Scope, Counter, Mark


mimetype_choices   = [
                      ('text/plain', u'text/plain'),
                      ('application/json', u'application/json'),
                     ]


class Snippet(UUIDModel):

    creator    = models.ForeignKey(User, related_name='metadata_snippets_created')
    user       = models.ForeignKey(User, db_index=True, related_name='metadata_snippets')
    visibility = models.SlugField(default='public', max_length=64,
                     choices=VISIBILITY_CHOICES)
    mimetype   = models.SlugField(db_index=True, default='text/plain', max_length=64,
                     choices=mimetype_choices)
    slug       = models.SlugField(db_index=True, max_length=128)
    type       = SlugBlankToNoneField(db_index=True, max_length=64, null=True, blank=True, default=None)
    content    = models.TextField()
    datetime   = models.DateTimeField(db_index=True, auto_now_add=True)

    # Models
    assigned_users      = models.ManyToManyField(User, db_index=True, null=True, blank=True,
                              related_name='assigned_metadata_snippets')
    assigned_units      = models.ManyToManyField(Unit, db_index=True, null=True, blank=True,
                              related_name='assigned_metadata_snippets')
    assigned_quantities = models.ManyToManyField(Quantity, db_index=True, null=True, blank=True,
                              related_name='assigned_metadata_snippets')
    assigned_scopes     = models.ManyToManyField(Scope, db_index=True, null=True, blank=True,
                              related_name='assigned_metadata_snippets')
    assigned_counters   = models.ManyToManyField(Counter, db_index=True, null=True, blank=True,
                              related_name='assigned_metadata_snippets')
    assigned_marks      = models.ManyToManyField(Mark, db_index=True, null=True, blank=True,
                              related_name='assigned_metadata_snippets')

    class Meta():

        ordering = ['-datetime',]

    def __unicode__(self):
        return u'%s | %s | %s | %s <%s> %s' % \
            (self.slug, self.mimetype, self.type, self.visibility, self.pk, self.user)
