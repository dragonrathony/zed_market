# payments/views.py
from django.conf import settings  # new
from django.views.generic.base import TemplateView
import stripe  # new
from django.shortcuts import render, redirect
from ads.models import AdList


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


def clean(data):
    if 'csrfmiddlewaretoken' in data:
        data.pop('csrfmiddlewaretoken')
    return data

def checkout(request, ad_id):
    data = dict(request.POST)
    data = clean(data)
    print(data)
    amount = data['basic'][0]
    print(amount)

    key = settings.STRIPE_TEST_PUBLIC_KEY
    print(key)
    user = request.user
    ads = AdList.objects.filter(pk=ad_id)[0]
    print(ads)
    return render(request, 'checkout.html', {"ad": ads, "user": user, 'key':key, 'amount':amount})


def buyer_pay(request, ad_id):  # new
    key = settings.STRIPE_TEST_PUBLIC_KEY
    user = request.user
    ads = AdList.objects.filter(pk=ad_id)[0]

    return render(request, 'checkout.html', {"ad": ads, "user": user, 'key':key})


def charge(request, ad_id):

    user = request.user
    data = {}
    ads = AdList.objects.filter(pk=ad_id)[0]
    print(ads)
    print(ads.featured_ad)
    ad_data = AdList.objects.filter(pk=ad_id).values()

    # updating ad status and payment status for the advertiser
    data['paid'] = True
    data['is_active'] = True
    AdList.objects.filter(pk=ad_id).update(**data)
    
    ad_price = ads.item_price
    total_amount = int(round(100 * ad_price))
    title = ads.title

    # if request.method == 'POST':
    #     print(request.POST['stripeToken'])
    #     charge = stripe.Charge.create(
    #         amount=total_amount,
    #         currency='inr',
    #         description=title,
    #         source=request.POST['stripeToken'])

    return render(request, 'charge.html', {"ad_price": ad_price, "user": user})

