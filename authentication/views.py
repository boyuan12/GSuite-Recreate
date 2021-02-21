from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import requests
from django.contrib.auth.models import User
from django.contrib.auth import login

BASE_URL = "http://127.0.0.1:8001/auth/sso/get_auth_token/"
ACCOUNT_SERVER_URL = "http://127.0.0.1:8000"

# Create your views here.
def register(request):
    return render(request, "authentication/register.html")


def auth_redirect(request):
    authentication_token = requests.post(f"{ACCOUNT_SERVER_URL}/auth/sso/request_authentication_token/")
    request.session["request_token"] = authentication_token.json()["authentication_token"]
    print(authentication_token.json()["authentication_token"])
    return redirect(f"{ACCOUNT_SERVER_URL}/auth/sso/authorization_request/?next={BASE_URL}&request_token={authentication_token.json()['authentication_token']}")


def get_auth_token(request):
    auth_token = request.GET["auth_token"]
    r = requests.post(f"{ACCOUNT_SERVER_URL}/auth/sso/verify_auth_token/", data={
        "auth_token": auth_token
    })

    user = User.objects.get(id=r.json()["user_id"])

    login(request, user)

    return redirect("/")

