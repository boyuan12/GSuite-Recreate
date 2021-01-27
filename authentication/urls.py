from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register),
    path("register/phone/", views.step_two_phone),
    path("register/phone-verify", views.phone_verify),
]