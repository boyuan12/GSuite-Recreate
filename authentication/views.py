from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from helpers import validate_password, random_str
import os
from twilio.rest import Client


TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

c = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

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

        return redirect("/register/phone/")

    return render(request, "authentication/register.html")


def step_two_phone(request):
    if request.method == "POST":
        
        country_code = request.POST["country-code"]
        phone = request.POST["phone"]
        code = random_str()


        c.messages.create(from_='+19162800623', body='TWOFA Code: ' + code, to='+' + country_code + phone)
        request.session["code"] = code

        return render(request, "authentication/phone-verify.html")

    else:
        return render(request, "authentication/phone.html")


def phone_verify(request):
    if request.method == "POST":
        return HttpResponse(request.POST["code"])



def login_view(request):
    pass


def logout_view(request):
    pass

