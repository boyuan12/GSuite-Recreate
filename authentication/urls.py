from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register),
    path("register/phone/", views.step_two_phone),
    path("phone-verify/", views.phone_verify),
    path("api/username/", views.api_check_username_exist),
    path("login/", views.login_view)
]