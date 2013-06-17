#!/usr/bin/env python
import os, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "traceparent.settings")

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')))

from tp_auth.models import User, LoginToken

user = User.objects.get(email__iexact=sys.argv[1])

LoginToken.objects.filter(user=user).delete()
token, created = LoginToken.objects.get_or_create(user=user)

print token.pk
