from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    return render(request, "authentication/register.html")


def login_view(request):
    pass


def logout_view(request):
    pass

