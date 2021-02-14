from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from helpers import validate_password, random_str, send_mail
import os
from twilio.rest import Client
from .models import ForgotPasswordToken, Profile, RequestToken, AuthToken
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json


TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

c = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

BASE_URL = "127.0.0.1:8000"

# Create your views here.
def register(request):
    # print(request.user.is_authenticated)
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
        request.session["query_string"] = request.GET.get("next") + "&next=" +request.GET.get("next_2")

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

        if request.session.get("query_string") != None:
            return redirect(request.session.get("query_string"))
        return HttpResponse("Welcome!")


def login_view(request):
    if request.user.is_authenticated:
        return render(request, "authentication/login.html", {
            "message": "You already logged in, please log out first.",
            "password": False
        })

    if request.method == "POST":

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
            print(request.GET.get("next"))

            user = authenticate(username=request.POST["username"], password=request.POST["password"])
            if user == None:
                return render(request, "authentication/login.html", {
                    "password": False,
                    "message": "Invalid credential, try again."
                })
            login(request, user)

            if not request.GET.get("next"):
                return HttpResponse("logged in successfullY!")
            return redirect(request.GET.get("next") + "&next=" +request.GET.get("next_2"))

    else:
        return render(request, "authentication/login.html", {
            "password": False
        })


def logout_view(request):
    logout(request)
    return render(request, "authentication/login.html", {
        "password": False
    })


@csrf_exempt
def request_authentication_request(request):
    RequestToken().save()
    auth_request = RequestToken.objects.filter()[::-1][0]
    return JsonResponse({"authentication_token": auth_request.code})


def authorization_request(request):
    request_token = request.GET["request_token"]
    print("request token", request_token)

    try:
        RequestToken.objects.filter(code=request_token)[0]
    except RequestToken.DoesNotExist:
        return JsonResponse({"error": "request token not valid"})

    next = request.GET["next"]

    if request.user.is_authenticated:
        AuthToken(user=request.user.id).save()
        auth_token = AuthToken.objects.filter(user=request.user.id)[::-1][0]
        return redirect(f"{next}?request_token={request_token}&auth_token={auth_token.code}")
    else:
        return redirect(f"/auth/login/?next=/auth/sso/authorization_request/?request_token={request_token}&next_2={next}")


@csrf_exempt
def verify_auth_token(request):
    auth_token = request.POST["auth_token"]

    try:
        at = AuthToken.objects.filter(code=auth_token)[0]
        return JsonResponse({"user_id": at.user})
    except AuthToken.DoesNotExist:
        return JsonResponse({"error": "auth token is invalid"})



def forgot_password_request(request):
    logout(request)

    if request.method == "POST":
        info = request.POST["info"]

        try:
            user = User.objects.get(email=info)
            ForgotPasswordToken(user=user.id).save()
            code = ForgotPasswordToken.objects.filter(user=user.id)[::-1][0].code
            send_mail(info, "Reset Your Password", f"Click this <a href='{BASE_URL}/auth/reset/{code}/'>link</a> to reset your password")
        except User.DoesNotExist:
            try:
                p = Profile.objects.get(phone=info)
                ForgotPasswordToken(user=p.user.id).save()
                code = ForgotPasswordToken.objects.filter(user=p.user.id)[::-1][0].code
                c.messages.create(from_='+19162800623', body=f"Password reset: {BASE_URL}/auth/reset/{code}/")
            except Profile.DoesNotExist:
                return render(request, "authentication/forgot-password.html", {
                    "message": "Email/Phone is not valid"
                })

    else:
        return render(request, "authentication/forgot-password.html")


def password_reset(request, code):
    logout(request)
    try:
        ForgotPasswordToken.objects.get(code=code)
    except ForgotPasswordToken.DoesNotExist:
        return render(request, "authentication/reset-password.html", {
            "message": "Code doesn't exist"
        })

    if request.method == "POST":
        user_id = ForgotPasswordToken.objects.get(code=code).user
        if request.POST["password"] != request.POST["confirmation"]:
            return render(request, "authentication/reset-password.html", {
                "message": "Confirm password doesn't match password"
            })

        if not validate_password(request.POST["password"]):
            return render(request, "authentication/reset-password.html", {
                "message": "Password didn't pass validation"
            })

        User.objects.get(id=user_id).set_password(request.POST["password"]).save()

        return redirect("/auth/login/")
    else:
        return render(request, "authentication/reset-password.html")

# @csrf_exempt
# def api_check_username_exist(request: HttpRequest):
#     if request.method == "POST":
#         if request.get_host() != BASE_URL:
#             return JsonResponse({"success": False, "valid": None})

#         print("Log: ", request.body)
#         data = json.loads(request.body.decode("utf-8"))
#         username = data["username"]

#         try:
#             User.objects.get(username=username)
#             return JsonResponse({"success": True, "valid": True})
#         except User.DoesNotExist:
#             return JsonResponse({"success": True, "valid": False})

