from django.contrib import admin
from django.urls import path
from .views import create_checkout_session, check_payment_status, expire_checkout_session
urlpatterns = [
    path('create-session/', create_checkout_session),
    path('check-payment-status/', check_payment_status),
    path('expire-checkout-session/', expire_checkout_session),
]
