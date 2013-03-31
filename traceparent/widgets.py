# -*- coding: utf-8 -*-
from django.forms import widgets
from django.utils.safestring import mark_safe

from rest_framework.reverse import reverse


class MultipleLockedInput(widgets.MultipleHiddenInput):

    model     = None
    view_name = None

    def __init__(self, *args, **kwargs):

        self.model     = kwargs.pop('model')
        self.view_name = kwargs.pop('view_name')

        return super(MultipleLockedInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):

        r = super(MultipleLockedInput, self).render(name, value, attrs=None)

        if not value: return r

        q = self.model.objects.get(pk=value[0])

        return mark_safe('%s<a href="%s" class="uneditable-input">%s</a>' % \
                   (r, reverse(self.view_name, (q.pk,)), q))
