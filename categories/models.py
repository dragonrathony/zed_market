from django.db import models
import os
from datetime import datetime
from .managers import CategoryManager


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class Category(models.Model):

    # additional
    category = models.CharField(max_length=100, null=True)
    subcategory = models.CharField(max_length=100, null=True)
    data_value = models.CharField(max_length=100, null=True)

    objects = CategoryManager()

    def __str__(self):
        return self.category
