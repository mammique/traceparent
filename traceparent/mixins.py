# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe


class DescActionMixin(object):

    description_actions = []

    def description_actions_add(self, action):

        self.description_actions_add.append(action)

    def get_description(self, *args, **kwargs):

        desc = super(DescActionMixin, self).get_description(*args, **kwargs)

        if kwargs.get('html'):

            lis = []

            for a in  self.description_actions:

                if callable(a[1]): href = a[1](self.object)
                else: href = a[1]

                lis.append('<li><a href="%s">%s</a></li>' % (href, a[0],))

            desc += """<div id="action" class="pull-right btn-group">""" \
                    """<a class="btn btn-primary dropdown-toggle" """ \
                    """data-toggle="dropdown" href="#">""" \
                    """Action <span class="caret"></span></a><ul class="dropdown-menu">""" \
                    """%s</ul></div>""" \
                    """<script id="action-move" type="text/javascript">""" \
                    """window.onload = function() { $('#action').prependTo('#content'); $('#action-move').remove()}""" \
                    """</script>""" % ''.join(lis)
            desc = mark_safe(desc)

        return desc



