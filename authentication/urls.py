from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register),
    path("register/phone/", views.step_two_phone),
    path("phone-verify/", views.phone_verify),
    # path("api/username/", views.api_check_username_exist),
    path("login/", views.login_view),
    path("sso/request_authentication_token/", views.request_authentication_request),
    path("sso/authorization_request/", views.authorization_request),
    path("sso/verify_auth_token/", views.verify_auth_token),
    path("logout/", views.logout_view),
    path("forgot-password/", views.forgot_password_request)
]