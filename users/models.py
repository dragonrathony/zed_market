from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

import os

from .managers import CustomUserManager


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    # mandatory fields
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(max_length=100)

    # additional
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    profile_image = models.CharField(max_length=100, null=True)
    user_name = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=100, null=True)
    contact_number = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)

    # admin roles
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    deactivate_msg = models.CharField(max_length=300, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

