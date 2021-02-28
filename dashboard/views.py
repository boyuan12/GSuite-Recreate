from django.shortcuts import render
from .models import Email
from django.http import HttpResponse
from helpers import send_mail, current_milli_time


# Create your views here.
def index(request):
    emails = Email.objects.filter(to_email=f"{request.user.username}@devwithme.xyz")
    data = [] # [from_email, to_email, subject, timestamp, name]
    for e in emails:
        name = e.from_email.split("<")[0]
        data.append([e.from_email, e.to_email, e.subject, e.timestamp, name])
    data.reverse()
    return render(request, "dashboard/index.html", {
        "emails": data
    })


def send(request):
    if request.method == "POST":
        send_mail(f"{request.user.username}@devwithme.xyz", request.POST["receiver"], request.POST["subject"], request.POST["body"])

        Email(timestamp=str(current_milli_time()), subject=request.POST["subject"], body=request.POST["body"], from_email=f"{request.user.username}@devwithme.xyz", to_email=request.POST["receiver"]).save()

        return HttpResponse("Sent successfully!")

    else:
        return render(request, "dashboard/send.html")


def view_email(request, ms):
    email = Email.objects.get(timestamp=ms, to_email=f"{request.user.username}@devwithme.xyz")
    return render(request, "dashboard/email.html", {
        "email": email
    })


def raw_email(request, ms):
    email = Email.objects.get(timestamp=ms, to_email=f"{request.user.username}@devwithme.xyz")
    response = HttpResponse(email.body)
    response["Content-Type"] = "text/html"
    return HttpResponse(email.body)
