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
from django.urls import path, include
from . import views


app_name = 'ads'

urlpatterns = [
    path('create/', views.create_ad_func, name='create'),
    path('create', views.create_ad_func, name='create_api'),
    path('list', views.list_ads_func, name='list'),
    path('grid', views.grid_ads_func, name='grid'),
    path('terms_condition/', views.terms_condition, name='terms_condition'),
    path('checkout/', include('payments.urls'), name='checkout'), # new
    path('<int:ad_id>', views.view_ad),
    path('edit/<int:ad_id>', views.edit_ad),
    path('delete/<int:ad_id>', views.delete_ad),
    path('search', views.search_ads_func),
    path('favourite_ad', views.favourite_ad, name='favourite_ad'),
    path('update/<int:ad_id>', views.update, name='update'),
    path('archive/', views.archive_ads, name='archive_ads'),
    path('subcategory/<str:category>', views.get_subcategory, name='subcategory'),
    path('search/<str:category>', views.subcategory_filtering, name='search'),
    # path('update_profile', views.update_profile, name='update_profile')
]

