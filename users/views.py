from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from django.http import HttpResponseRedirect
from users.models import CustomUser as User
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth import authenticate
from pprint import pprint
from zed_market.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from ads.models import AdList

from .forms import ProfileForm
# from django.contrib.auth.models import User
#

def clean(data) :
    Data = {}
    for (k,v) in data.items() :
        Data[k] = v[0]
    if 'csrfmiddlewaretoken' in Data:
            Data.pop('csrfmiddlewaretoken')
    return Data

def create_user():
    user_data = Users.objects.all()
    print(user_data)


def register(request):
    if request.method == 'POST':
        f = forms.EmailField()
        if f.clean(request.POST.get('email')):
            email = request.POST.get('email')
            password = request.POST.get('password')

            try:
                user = User.objects.create_user(email, password)
                user.save()
                return render(request, 'login.html', {})

            except Exception as e:
                print('*'*20, e)
                message = 'This email is already registered, use another email!'
                user = False
                return render(request, 'register.html', {'message': message, 'user':user})

    return render(request, 'register.html', {})


def login(request):
    next = request.GET.get('next')
    user = ''
    state = 'Please Login here'
    print(next)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = authenticate(email=email, password=password)
        except Exception as e:
            user = None
            print('*'*20, e)
 
        if user is not None:
            if user.is_active:
                django_login(request, user)
                state = "You're successfully logged in!"
                next = request.POST.get('next')
                print(user, next)
                if next is not None:
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponseRedirect(next)
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

        return render(request,
                      'login.html',
                      {
                          'state': state,
                          'username': user,
                          'next': next,
                      })

    else:
        if next is None :
            next = '/'
        return render(request, 'login.html',
                      {
                          'state': state,
                          'username': user,
                          'next': next,
                      })


def handle_uploaded_file(f, pk):
    fn = 'static_in_env/images/user/{}.jpg'.format(pk)
    with open(fn, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    fn = 'static/images/user/{}.jpg'.format(pk)
    with open(fn, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    fn = '/static/images/user/{}.jpg'.format(pk)
    return fn


def update_profile(request):
    user = request.user
    print(user)
    data = dict(request.POST)
    data = clean(data)
    pprint(data)

    # updating image of the user
    if len(request.FILES) > 0:
        print(len(request.FILES))
        if 'profile_image' in request.FILES :
            fn = handle_uploaded_file(request.FILES['profile_image'], user.id)
            data['profile_image'] = fn
        print('going to update')
    else:
        del data['profile_image']

    # updating password
    if 'current_password' in data:
        if data['new_password1'] == data['new_password2']:
            # user_data = User.objects.filter(pk=user.id).values()
            data['password'] = data['new_password1']
            del data['new_password1']
            del data['new_password2']
            del data['current_password']
        else:
            print('incorrect password')
        pprint(data)

    if 'current_email' in data:
        if data['current_email'] == user.email:
            data['email'] = data['new_email']
            del data['current_email']
            del data['new_email']
            AdList.objects.filter(email=user.email).update(**data)
        else:
            print('incorrect email' )
        pprint(data)

    pprint(data)
    User.objects.update_user(user.id, data)
    return redirect('/user_profile')


def logout(request):
    django_logout(request)
    return redirect('/')


def delete_account(request):
    user = request.user
    data = {}
    print(user)
    instance = User.objects.filter(email=request.user.email).values()
    ads = AdList.objects.filter(email=request.user.email).values()
    data['is_active'] = False
    print(data)
    print(instance[0])
    AdList.objects.filter(email=request.user.email).values()
    for ad in ads:
        AdList.objects.filter(pk=ad['id']).update(**data)
    pprint(instance[0]['id'])
    User.objects.update_user(instance[0]['id'], data)
    return redirect('/users/logout')


def contact_seller(request):
    user = request.user.email
    data = dict(request.POST)
    data = clean(data)

    if request.method == 'POST':
        subject = 'Enquiry for {} category!'.format(data['category'])
        message = data['message']
        recepient = str(user)
        print(subject, message, recepient)
        send_mail(subject,
            message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        if send_mail:
            message = True
            return render(request, 'seller.html', {'message':message})
        else:
            message = False
            return render(request, 'contact-us.html')
            return render(request, 'seller.html', {'message':message})

    return render(request, 'seller.html', {})


def handler404(request, exception, template_name="404.html"):
    response = render(request, "404.html")
    response.status_code = 404
    return response


def handler500(request):
    return render(request, '500.html', status=500)