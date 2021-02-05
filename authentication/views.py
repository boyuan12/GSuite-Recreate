from django.shortcuts import render, redirect
import requests

BASE_URL = "http://127.0.0.1:8001"
ACCOUNT_SERVER_URL = "http://127.0.0.1:8000"

# Create your views here.
def register(request):
    return render(request, "authentication/register.html")


def auth_redirect(request):
    authentication_token = requests.post(f"{ACCOUNT_SERVER_URL}/auth/sso/request_authentication_token/")
    request.session["authentication_token"] = authentication_token.json()["authentication_token"]
    print(authentication_token.json()["authentication_token"])
    return redirect(f"{ACCOUNT_SERVER_URL}/auth/sso/?next={BASE_URL}")

