from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from helpers import validate_password, random_str
import os
from twilio.rest import Client
from .models import Profile
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json


TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

c = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

BASE_URL = "127.0.0.1:8000"

# Create your views here.
def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # check password match confirmation
        if password != confirmation:
            return render(request, "authentication/register.html", {
                "message": "Please double your password and confirmation, they must match each other"
            })

        # check password match requirement (1 lowercase letter, 1 uppercase letter, 1 number, 1 special char)
        if validate_password(password) == False:
            return render(request, "authentication/register.html", {
                "message": "Your password must be between 8-20 characters long, have at least 1 each: lowercase letter, uppercase letter, digit, special character"
            })


        # check if user already exist
        try:
            User.objects.get(username=username)
            return render(request, "authentication/register.html", {
                "message": f"Username: {username} already exist."
            })

        except User.DoesNotExist:
            pass

        request.session["username"] = username
        request.session["password"] = password
        request.session["first_name"] = first_name
        request.session["last_name"] = last_name

        return redirect("/auth/register/phone/")

    return render(request, "authentication/register.html")


def step_two_phone(request):
    if request.method == "POST":

        country_code = request.POST["country-code"]
        phone = request.POST["phone-number"]
        code = random_str()

        print(code)

        c.messages.create(from_='+19162800623', body='TWOFA Code: ' + code, to='+' + country_code + phone)
        request.session["code"] = code
        request.session["phone"] = '+' + country_code + phone

        return render(request, "authentication/phone-verify.html")

    else:
        return render(request, "authentication/phone.html")


def phone_verify(request):
    if request.method == "POST":
        if request.session.get("code") != request.POST["code"]:
            return render(request, "authentication/phone.html", {
                "message": "Invalid code"
            })

        User.objects.create_user(username=request.session.get("username"), password=request.session.get("password"), first_name=request.session.get("first_name"), last_name=request.session.get("last_name"))

        user = User.objects.get(username=request.session.get("username"))

        Profile(user=user, phone=request.session.get("phone")).save()

        return HttpResponse("Welcome!")


def login_view(request):
    if request.method == "POST":
        print(request.POST)
        if not request.POST.get("password"):
            username = request.POST["username"]
            try:
                User.objects.get(username=username)
                return render(request, "authentication/login.html", {
                    "password": True,
                    "username": username
                })
            except User.DoesNotExist:
                return render(request, "authentication/login.html", {
                    "message": "Username Invalid",
                    "password": False
                })

        else:
            user = authenticate(username=request.POST["username"], password=request.POST["password"])
            if user == None:
                return render(request, "authentication/login.html", {
                    "password": False,
                    "message": "Invalid credential, try again."
                })
            login(request, user)
            return HttpResponse("logged in successfullY!")

    else:
        return render(request, "authentication/login.html", {
            "password": False
        })


def logout_view(request):
    pass


@csrf_exempt
def api_check_username_exist(request: HttpRequest):
    if request.method == "POST":
        if request.get_host() != BASE_URL:
            return JsonResponse({"success": False, "valid": None})

        print("Log: ", request.body)
        data = json.loads(request.body.decode("utf-8"))
        username = data["username"]

        try:
            User.objects.get(username=username)
            return JsonResponse({"success": True, "valid": True})
        except User.DoesNotExist:
            return JsonResponse({"success": True, "valid": False})

