# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe


class DescActionMixin(object):

    description_actions = []

    def description_actions_add(self, action):

        self.description_actions_add.append(action)

    def get_description(self, *args, **kwargs):

        desc = super(DescActionMixin, self).get_description(*args, **kwargs)

        if kwargs['html']:

            lis = []
#            actions = [] + map(lambda x: list(x), self.description_actions)

            for a in  self.description_actions:

                if callable(a[1]): href = a[1](self.object)
                else: href = a[1]

                lis.append('<li><a href="%s">%s</a></li>' % (href, a[0],))

#                print a, callable(a[1])

            desc += """<div class="btn-group">""" \
                    """<a class="btn btn-primary dropdown-toggle" """ \
                    """data-toggle="dropdown" href="#">""" \
                    """Action <span class="caret"></span></a><ul class="dropdown-menu">""" \
                    """%s</ul></div>""" % ''.join(lis)
            desc = mark_safe(desc)

        return desc



