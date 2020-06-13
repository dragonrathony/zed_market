from django.conf import settings  # new
import stripe  # new
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from ads.models import AdList
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth import authenticate
from pprint import pprint
from django.db.models import F
from django.db.models import Q
from django.contrib.postgres.search import SearchVector
from reviews.models import Reviews
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from categories.models import Category
import json

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


@login_required(login_url='/users/login')
def create_ad_func(request):
    user = request.user
    if request.method == "POST":

        data = dict(request.POST)
        pprint(data)
        data = clean(data)
        ad = AdList.objects.create_ad(**data)
        img_counter = 0
        featured_ad_status = ad.featured_ad

        for ad_img in request.FILES:
            print(ad_img)
            print(img_counter)
            print(request.FILES[ad_img])
            fn = handle_uploaded_file(request.FILES[ad_img], ad.id, img_counter)
            img_counter = img_counter + 1
            data[ad_img] = fn
        AdList.objects.filter(pk=ad.id).update(**data)
        pprint(data)
        print(ad.id)

        print(featured_ad_status)

        return render(request, 'package.html', {"user": request.user, 'ad': ad, 'featured_ad':featured_ad_status})
    else:
        return render(request, 'Ad-listing.html', {"user": request.user})


def handle_uploaded_file(f, pk, img_counter):

    if img_counter == 0:
        fn = 'static_in_env/images/ads/{}.jpg'.format(pk)
    else:
        fn = 'static_in_env/images/ads/{}_{}.jpg'.format(pk, img_counter)

    with open(fn, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    if img_counter == 0:
        fn = 'static/images/ads/{}.jpg'.format(pk)
    else:
        fn = 'static/images/ads/{}_{}.jpg'.format(pk, img_counter)

    with open(fn, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    fn = '/' + fn
    print(fn)
    return fn


def list_ads_func(request):
    user = request.user

    filters = dict(request.GET)
    filters = clean(filters)

    if not 'price_min' in filters:
        filters['price_min'] = -1
    if not 'price_max' in filters:
        filters['price_max'] = 1000000

    if 'shortby' in filters:
        if filters['shortby']  == 'Lowest Price':
            filters['price_min'] = 0
            filters['price_max'] = 500
        elif filters['shortby']  == 'Highest Price':
            filters['price_min'] = 500
            filters['price_max'] = 100000

    filters['price_min'] = int(filters['price_min'])
    filters['price_max'] = int(filters['price_max'])
    print(filters['price_min'], filters['price_max'])

    ads = AdList.objects.filter(is_active=True, item_price__gte=filters['price_min'], item_price__lte=filters['price_max']).values()

    for ad in ads:
        rating_list = []
        review_data = Reviews.objects.filter(ad_id=ad['id'])
        
        for review in review_data:
            stars = review.ad_rating
            rating_list.append(stars)

        if len(rating_list) > 0:
            average_rating = round(sum(rating_list) / len(rating_list))
            ad['rating'] = average_rating
        else:
            ad['rating'] = 0

    paginator = Paginator(ads, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = AdList.objects.filter(is_active=True).values('subcategory')

    location = AdList.objects.values('zip_code')
    print((data))
    data2 = []
    location_list = []

    for loc in location:
        address = loc['zip_code']
        if address != None:
            ok = address.replace(" ", "") 
            location_list.append(ok)

    for cats in data:
        sub = cats['subcategory']
        if sub != None:
            data2.append(sub)

    my_dict = {i:data2.count(i) for i in data2}
    location_dict = {i:location_list.count(i) for i in location_list}
    
    if 'None' in location_dict:
        location_dict['None'] = 0
        
    return render(request, 'ad-list-view.html', {"ads": page_obj, 'ads_number': my_dict, 'location':location_dict})


def grid_ads_func(request):
    user = request.user
    filters = dict(request.GET)
    filters = clean(filters)
    print('this is where i am getting the data.....', filters)

    if not 'price_min' in filters:
        filters['price_min'] = -1
    if not 'price_max' in filters:
        filters['price_max'] = 1000000

    if 'shortby' in filters:
        if filters['shortby']  == 'Lowest Price':
            filters['price_min'] = 0
            filters['price_max'] = 500
        elif filters['shortby']  == 'Highest Price':
            filters['price_min'] = 500
            filters['price_max'] = 100000

    filters['price_min'] = int(filters['price_min'])
    filters['price_max'] = int(filters['price_max'])

    ads = AdList.objects.filter(is_active=True, item_price__gte=filters['price_min'], item_price__lte=filters['price_max']).values()

    for ad in ads:
        rating_list = []
        review_data = Reviews.objects.filter(ad_id=ad['id'])
        
        for review in review_data:
            stars = review.ad_rating
            rating_list.append(stars)

        if len(rating_list) > 0:
            average_rating = round(sum(rating_list) / len(rating_list))
            ad['rating'] = average_rating
        else:
            ad['rating'] = 0

    paginator = Paginator(ads, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = AdList.objects.filter(is_active=True).values('subcategory')

    location = AdList.objects.values('zip_code')
    print((data))
    data2 = []
    location_list = []

    for loc in location:
        address = loc['zip_code']
        if address != None:
            ok = address.replace(" ", "") 
            location_list.append(ok)
            print(ok)


    for cats in data:
        sub = cats['subcategory']
        if sub != None:
            print(sub)
            data2.append(sub)

    print(data2)
    my_dict = {i:data2.count(i) for i in data2}
    location_dict = {i:location_list.count(i) for i in location_list}

    if 'None' in location_dict:
        location_dict['None'] = 0

    return render(request, 'ad-grid-view.html', {"ads": page_obj, 'ads_number': my_dict, 'location':location_dict})


@login_required(login_url='/users/login')
def terms_condition(request):
    return render(request, 'terms-condition.html', {})


def view_ad(request, ad_id):
    user = request.user
    print(ad_id)
    ad_data = AdList.objects.filter(pk=ad_id)[0]
    review_data = Reviews.objects.filter(ad_id=ad_id)

    return render(request, 'ad_view.html', {"user": user, "ad": ad_data, 'reviews' : review_data})
    # return render(request, 'ad_view.html', {"user": user, "ad": ad_data})


def delete_ad(request, ad_id):
    instance = AdList.objects.filter(email=request.user, pk=ad_id)[0]
    instance.delete()

    data = {}
    email = request.user.email
    ads = AdList.objects.filter(email=email, is_active=True).values()
    my_ads = AdList.objects.filter(email=email, is_active=True).values()
    featured_ad = AdList.objects.filter(email=email, is_active=True, featured_ad=True).values()
    archive_ad = AdList.objects.filter(email=email, is_active=False).values()

    data = {
      "my_ads": len(my_ads),
      "featured_ad": len(featured_ad),
      "archive_ad" : len(archive_ad),
    }
    print(data)

    paginator = Paginator(ads, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard.html', {"user":request.user, "ads":page_obj, "ads_number":data})


def edit_ad(request, ad_id):
    user = request.user
    ad = AdList.objects.filter(pk=ad_id)[0]
    # print(ad.premium_options)
    data = dict(request.POST)
    data = clean(data)
    if request.method == "POST":
        data = dict(request.POST)
        data = clean(data)

        img_counter = 0
        featured_ad_status = ad.featured_ad
        
        if len(request.FILES) > 0:
            for ad_img in request.FILES:
                print(ad_img)
                print(img_counter)
                print(request.FILES[ad_img])
                fn = handle_uploaded_file(request.FILES[ad_img], ad.id, img_counter)
                img_counter = img_counter + 1
                data[ad_img] = fn
        else:
            data['ad_img'] = '/static/images/ads/{}.jpg'.format(ad.id)
            
        AdList.objects.filter(pk=ad.id).update(**data)
        featured_ad_status = ad.featured_ad
        print('featured_ad_status', featured_ad_status)

        ad_data = AdList.objects.filter(pk=ad.id).values()[0]
        print(ad_data)

        if ad_data['is_active'] is True:
            return redirect('/ads/list')
        else:
            ad_id = ad_data['id']
            print(ad_data['is_active'], ad_id)
            print(featured_ad_status)
            return render(request, 'package.html', {"user": request.user, 'ad': ad, 'featured_ad':featured_ad_status})
    else:
        return render(request, 'ad_edit.html', {"user": user, "ad": ad})


def search_ads_func(request):

    if request.method == 'POST':
        filters = dict(request.POST)
        filters = clean(filters)
        pprint(filters)

        category_searched = filters['category']
        location_searched = filters['location']
        text_searched = filters['search_text']

        print(category_searched, location_searched, text_searched)

        if category_searched == 'Lowest Price':
            filters['price_min'] = -1
            filters['price_max'] = 500
        elif category_searched == 'Highest Price':
            filters['price_min'] = 500
            filters['price_max'] = 100000
        else:
            filters['price_min'] = 0
            filters['price_max'] = 100000

        ads = AdList.objects.filter(subcategory__icontains=text_searched, item_price__gte= filters['price_min'], item_price__lte=filters['price_max'], zip_code__icontains=location_searched) 
        
        paginator = Paginator(ads, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'ad-grid-view.html', {'ads':ads})
    else:
        ads = AdList.objects.filter(item_price__gte= 1, item_price__lte=100000) 
        paginator = Paginator(ads, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'ad-grid-view.html', {"ads": page_obj, "user": user})


def favourite_ad(request):
    data = {}
    email = request.user.email
    ads = AdList.objects.filter(email=email, is_active=True, featured_ad=True).values()
    my_ads = AdList.objects.filter(email=email, is_active=True).values()
    featured_ad = AdList.objects.filter(email=email, is_active=True, featured_ad=True).values()
    archive_ad = AdList.objects.filter(email=email, is_active=False).values()

    data = {
      "my_ads": len(my_ads),
      "featured_ad": len(featured_ad),
      "archive_ad" : len(archive_ad),
    }
    print(data)

    paginator = Paginator(ads, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard.html', {"user":request.user, "ads":page_obj, "ads_number":data})


def update(request, ad_id):
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
    key = settings.STRIPE_TEST_PUBLIC_KEY

    data = dict(request.POST)
    data = clean(data)
    pprint(data)
    AdList.objects.filter(pk=ad_id).update(**data)
    ads = AdList.objects.filter(pk=ad_id)[0]
    pprint(ads)

    return render(request, 'ad_view.html', {'ad': ads, 'key':key})


def archive_ads(request):
    data = {}
    email = request.user.email
    ads = AdList.objects.filter(email=email, is_active=False).values()
    my_ads = AdList.objects.filter(email=email, is_active=True).values()
    featured_ad = AdList.objects.filter(email=email, is_active=True, featured_ad=True).values()
    archive_ad = AdList.objects.filter(email=email, is_active=False).values()

    data = {
      "my_ads": len(my_ads),
      "featured_ad": len(featured_ad),
      "archive_ad" : len(archive_ad),
    }
    print(data)

    paginator = Paginator(ads, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard.html', {"user":request.user, "ads":page_obj, "ads_number":data})


def get_subcategory(request, category):

    subcategories = Category.objects.filter(category=category)
    data = {}
    for cats in subcategories:
        subcategory = cats.subcategory
        data_value = cats.data_value
        data[data_value] = subcategory

    json_str = json.dumps(data)
    print(json_str)
    return HttpResponse(json_str)


def subcategory_filtering(request, category):
    user = request.user
    print('*'*50,category)
    data = AdList.objects.values('subcategory')
    sub_cat_list = []

    for d in data:
        cat = d['subcategory']
        if cat != None:
            sub_cat_list.append(cat)

    if category in sub_cat_list:
        ads = AdList.objects.filter(subcategory__icontains=category, is_active=True)
    else:
        ads = AdList.objects.filter(zip_code__icontains=category, is_active=True)

    print(len(ads))
    
    paginator = Paginator(ads, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = AdList.objects.values('subcategory')
    location = AdList.objects.values('zip_code')
    print((data))
    data2 = []
    location_list = []

    for loc in location:
        address = loc['zip_code']
        if address != None:
            ok = address.replace(" ", "") 
            location_list.append(ok)
            print(ok)


    for cats in data:
        sub = cats['subcategory']
        if sub != None:
            print(sub)
            data2.append(sub)

    print(data2)
    my_dict = {i:data2.count(i) for i in data2}
    location_dict = {i:location_list.count(i) for i in location_list}
    print(my_dict)
    print(location_dict)

    return render(request, 'ad-grid-view.html', {"ads": page_obj, "user": user, 'ads_number': my_dict, 'location':location_dict})

