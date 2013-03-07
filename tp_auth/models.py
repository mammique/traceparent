# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

from django_extensions.db.fields import UUIDField

from rest_framework.authtoken.models import Token


# https://docs.djangoproject.com/en/1.5/topics/auth/customizing/#a-full-example
class UserManager(BaseUserManager):

    def create_user(self, email, password=None):

        if not email: raise ValueError('Users must have an email address')

        user = self.model(email=UserManager.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):

        user              = self.create_user(email, password=password)
        user.is_staff     = True
        user.is_active    = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractUser):

    uuid            = UUIDField(auto=True, primary_key=True)
    id              = UUIDField() # It appears that Django needs an 'id' on the `User` model.
    creator         = models.ForeignKey('self', null=True)
    name            = models.CharField(max_length=64, blank=True)
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def placeholder(self): return self.email == ''

    def save(self, *args, **kwargs):

        # 'username' must be unique and 'id' must be provided, let's mirror them with 'uuid'.
        if not self.uuid: self.uuid = self._meta.get_field("uuid").create_uuid()
        if self.username != self.uuid: self.username = self.uuid
        if self.id != self.uuid: self.id = self.uuid

        return super(User, self).save(*args, **kwargs)

    def __unicode__(self):

        if self.name:
            
            if self.email: return "%s <%s>" % (self.name, self.pk)
            else: return "%s *%s*" % (self.name, self.pk) # Mark symbolic `Users` with '*'.

        else: return '<%s>' % self.pk

    def __str__(self): return self.__unicode__()

# Monkey patch 'username' to match 'uuid' length.
User._meta.get_field("username").max_length = 36


# https://github.com/tomchristie/django-rest-framework/blob/17000129e35b10c9d08497a669fd72f8233f065a/rest_framework/authtoken/models.py#L1
import uuid
import hmac
from hashlib import sha1

class LoginToken(models.Model):

    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(User, related_name='auth_login_token')
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(LoginToken, self).save(*args, **kwargs)

    def generate_key(self):
        unique = uuid.uuid4()
        return hmac.new(unique.bytes, digestmod=sha1).hexdigest()

    def __unicode__(self):
        return self.key
