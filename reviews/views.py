from django.conf import settings  # new
import stripe  # new
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from django.http import HttpResponseRedirect
from ads.models import AdList
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth import authenticate
from pprint import pprint
from django.db.models import F
from django.contrib.postgres.search import SearchVector
from reviews.models import Reviews
from pprint import pprint
import arrow
from django.utils import timezone


from django.contrib.auth.decorators import login_required


def clean(data):
    Data = {}
    for (k, v) in data.items():
        if 'price' in k:
            if v[0].strip() == "":
                pass
            else:
                Data[k] = float(v[0])
        elif k == "negotiable":
            if v[0] == "Negotiable":
                Data[k] = True
            else:
                Data[k] = False
        else:
            Data[k] = v[0]
    if 'csrfmiddlewaretoken' in Data:
        Data.pop('csrfmiddlewaretoken')
    return Data


def create_review_func(request, ad_id):
    user = request.user
    if request.method == "POST":

        data = dict(request.POST)
        data = clean(data)

        ad_data = AdList.objects.filter(pk=ad_id)[0]
        print('*********', ad_data.item_price)
        
        data['ad_id'] = ad_id
        data['seller_email'] = ad_data.email
        data['item_price'] = ad_data.item_price
        data['post_date'] = timezone.now()

        pprint(data)
        review = Reviews.objects.create_review(**data)
        review_data = Reviews.objects.filter(ad_id=ad_id)

        return render(request, 'ad_view.html', {"user": user, "ad": ad_data, 'reviews' : review_data})

