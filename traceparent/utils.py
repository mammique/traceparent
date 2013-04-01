# -*- coding: utf-8 -*-
import re
from django.utils.datastructures import SortedDict


re_blank            = re.compile('[\t\n\r\f\v ]+')
re_blank_startswith = re.compile('^[\t\n\r\f\v ]+')
re_blank_endswith   = re.compile('[\t\n\r\f\v ]+$')


def blanks_prune(txt):

    return re_blank_endswith.sub('', re_blank_startswith.sub('', re_blank.sub(' ', txt)))


def ordered_dict(d): return SortedDict(sorted(d.items(), key=lambda x: x[0]))
