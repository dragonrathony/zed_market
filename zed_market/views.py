
from zed_market.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from reviews.models import Reviews
from ads.models import AdList
import json
from django.core.paginator import Paginator
from pprint import pprint
from categories.models import Category


def clean(data):
    Data = data
    if 'csrfmiddlewaretoken' in Data:
        Data.pop('csrfmiddlewaretoken')
    return Data


def index(request):
    ads = AdList.objects.filter(is_active=True, featured_ad=True).values()
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

    data = AdList.objects.filter(is_active=True).values('subcategory')
    print((data))
    data2 = []
    for cats in data:
        sub = cats['subcategory']
        if sub != None:
            print(sub)
            data2.append(sub)

    print(data2)
    my_dict = {i:data2.count(i) for i in data2}
    print(my_dict)

    return render(request, 'index.html', {"user":request.user, "ads":ads, 'ads_number':my_dict})


def about_us(request):
    return render(request, 'about-us.html', {})


@login_required(login_url='/users/login')
def ad_listing(request):
    return render(request, 'Ad-listing.html', {})


@login_required(login_url='/users/login')
def ad_list_view(request):
    return render(request, 'ad-list-view.html', {})


def blog(request):
    return render(request, 'blog.html', {})


def category(request):
    return render(request, 'category.html', {})


def contact_us(request):
    user = request.user.email
    data = dict(request.POST)
    data = clean(data)
    pprint(data)
    print(EMAIL_HOST_USER)

    if request.method == 'POST':
        subject = 'Enquiry for {} category!'.format(data['category'][0])
        message = data['message'][0]
        recepient = str(user)
        print(subject, message, recepient)
        send_mail(subject, 
            message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        if send_mail:
            message = True
            return render(request, 'contact-us.html', {'message':message}) 
        else:
            message = False
            return render(request, 'contact-us.html', {'message':message})

    return render(request, 'contact-us.html', {})


@login_required(login_url='/users/login')
def dashboad_archived_ads(request):
    return render(request, 'dashboard-archived-ads.html', {})

@login_required(login_url='/users/login')
def dashboad_favourit_ads(request):
    return render(request, 'dashboard-favourite-ads.html', {})

@login_required(login_url='/users/login')
def dashboad_my_ads(request):
    return render(request, 'dashboard-my-ads.html', {})

@login_required(login_url='/users/login')
def dashboad_pending_ads(request):
    return render(request, 'dashboard-pending-ads.html', {})

@login_required(login_url='/users/login')
def dashboard(request):
    data = {}
    email = request.user.email
    ads = AdList.objects.filter(email=email, is_active=True).values()
    featured_ad = AdList.objects.filter(email=email, is_active=True, featured_ad=True).values()
    archive_ad = AdList.objects.filter(email=email, is_active=False).values()

    data = {
      "my_ads": len(ads),
      "featured_ad": len(featured_ad),
      "archive_ad" : len(archive_ad),
    }
    

    paginator = Paginator(ads, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard.html', {"user":request.user, "ads":page_obj, "ads_number":data})

@login_required(login_url='/users/login')
def package(request):
    return render(request, 'package.html', {})

@login_required(login_url='/users/login')

def single_blog(request):
    return render(request, 'single-blog.html', {})


def test_ads(request):
    return render(request, 'single.html', {})


def store(request):
    return render(request, 'store.html', {})


@login_required(login_url='/users/login')
def user_profile(request):
    return render(request, 'user-profile.html', {'user': request.user})


# Uploading subcategories list to thier subsequent categories..
def _save_subcategories():

    print('*'*30)
    print('Uploading subcategories to category table. . .')

    with open("test.json", "rb") as f:
        json_data = json.load(f)

    for data in json_data:
        obj = Category.objects.create(category=data['category'], subcategory=data['subcategory'], data_value=data['data_value'])
        obj.save()
    print('subcategories are saved to thier subsequent categories!!')
    print('\n')

