# -*- coding: utf-8 -*-
from django.db import models

from django_extensions.db.fields import UUIDField


class UUIDModel(models.Model):

    uuid = UUIDField(auto=True, primary_key=True)

    class Meta:

        abstract = True

    def save(self, *args, **kwargs):

        # Needs an primary key prior to saving the 'ManyToManyField' field.
        if not self.uuid: self.uuid = self._meta.get_field("uuid").create_uuid()

        # FIXME: Or ._meta.model?
        super(UUIDModel, self).save(*args, **kwargs)
