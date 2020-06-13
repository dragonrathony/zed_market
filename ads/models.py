from django.db import models
from django.utils import timezone
import os
from datetime import datetime
from .managers import AdListManager


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class AdList(models.Model):

    # additional
    title = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100, null=True)
    subcategory = models.CharField(max_length=100, null=True)
    ad_type = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=1000, null=True)
    item_price = models.FloatField()
    ad_img = models.CharField(max_length=1000, null=True)
    ad_img2 = models.CharField(max_length=1000, null=True)
    ad_img3 = models.CharField(max_length=1000, null=True)
    ad_img4 = models.CharField(max_length=1000, null=True)
    ad_img5 = models.CharField(max_length=1000, null=True)

    buyer_name = models.CharField(max_length=1000, null=True)
    buyer_email = models.CharField(max_length=1000, null=True)
    review = models.CharField(max_length=1000, null=True)
    ad_rating = models.IntegerField(default=0)

    negotiable = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    amount_paid = models.IntegerField(default=0)
    featured_ad = models.BooleanField(default=False)
    term_conditions = models.BooleanField(default=False)

    post_date = models.DateTimeField(default=timezone.now)
    email = models.CharField(max_length=100, null=False)
    first_name = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)

    contact_number = models.CharField(max_length=20, null=True)

    premium_options = models.CharField(max_length=100, null=False)
    payment_method = models.CharField(max_length=100, default='CARD')

    objects = AdListManager()

    def __str__(self):
        return self.email
