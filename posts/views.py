from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from ads.models import AdList
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from categories.models import Category
from posts.models import Post
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


def create_post_func(request):
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


def list_post_func(request):
	post = Post.objects.list_post('Electronics')
	print(post)
	return render(request, 'single-blog.html', {})
