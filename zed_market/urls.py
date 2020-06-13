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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls import handler404, handler500
from .views import ( 
    index,
    about_us,
    ad_listing,
    ad_list_view,
    blog,
    category,
    contact_us,
    dashboad_archived_ads,
    dashboad_favourit_ads,
    dashboad_my_ads,
    dashboad_pending_ads,
    dashboard,
    package,
    single_blog,
    test_ads,
    store,
    user_profile,
    _save_subcategories, 
    )   


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('blog/', blog),
    path('about_us/', about_us),
    path('category/', category),
    path('contact_us/', contact_us),
    path('dashboad_archived_ads/', dashboad_archived_ads),
    path('dashboard/', dashboard),
    path('dashboad_favourit_ads/', dashboad_favourit_ads),
    path('dashboad_my_ads/', dashboad_my_ads),
    path('dashboad_pending_ads/', dashboad_pending_ads),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    path('payments/', include('payments.urls'), name='payments'),
    path('reviews/', include('reviews.urls'), name='reviews'),

    path('posts/', include('posts.urls'), name='posts'),
    path('users/', include('users.urls')),
    path('ads/', include('ads.urls')),
    path('package/', package),
    path('single_blog/', single_blog),
    path('store/', store),
    path('user_profile/', user_profile),
    path('test/', test_ads),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    ]

handler404 = 'users.views.handler404'
handler500 = 'users.views.handler500'
# subcategory = _save_subcategories()

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
