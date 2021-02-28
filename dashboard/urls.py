from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("send/", views.send),
    path("email/<str:ms>/", views.view_email),
    path("email/raw/<str:ms>/", views.raw_email)
]