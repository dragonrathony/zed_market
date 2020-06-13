"""zed_market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views


app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('login', views.login, name='login'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('seller', views.contact_seller, name='contact_seller'),
]

