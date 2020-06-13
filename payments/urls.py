# payments/urls.py
from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
    path('charge/<int:ad_id>', views.charge, name='charge'), # new
    path('checkout/<int:ad_id>', views.checkout, name='checkout'),
    path('buyer_pay/<int:ad_id>', views.buyer_pay, name='buyer_pay'),
]