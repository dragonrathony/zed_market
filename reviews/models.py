from django.db import models
from django.utils import timezone
import os
from datetime import datetime
from .managers import ReviewsManager
import arrow


class Reviews(models.Model):

    ad_id = models.IntegerField(default=0)
    seller_email = models.CharField(max_length=100, null=True)
    item_price = models.FloatField()

    buyer_name = models.CharField(max_length=1000, null=True)
    buyer_email = models.CharField(max_length=1000, null=True)
    review = models.CharField(max_length=1000, null=True)
    ad_rating = models.IntegerField(default=0)

    paid = models.BooleanField(default=False)
    post_date = models.DateTimeField(default=timezone.now)

    payment_method = models.CharField(max_length=100, null=True)

    objects = ReviewsManager()

    def __str__(self):
        return self.buyer_name
