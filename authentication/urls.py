from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register),
    path("redirect/", views.auth_redirect),
    path("sso/get_auth_token/", views.get_auth_token),
]