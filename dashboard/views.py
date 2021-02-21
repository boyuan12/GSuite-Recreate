from django.shortcuts import render
from .models import Email
from django.http import HttpResponse
from helpers import send_mail, current_milli_time


# Create your views here.
def index(request):
    emails = Email.objects.filter(to_email=f"{request.user.username}@devwithme.xyz")
    return render(request, "dashboard/index.html", {
        "emails": emails
    })


def send(request):
    if request.method == "POST":
        send_mail(f"{request.user.username}@devwithme.xyz", request.POST["receiver"], request.POST["subject"], request.POST["body"])

        Email(timestamp=str(current_milli_time()), subject=request.POST["subject"], body=request.POST["body"], from_email=f"{request.user.username}@devwithme.xyz", to_email=request.POST["receiver"]).save()

        return HttpResponse("Sent successfully!")

    else:
        return render(request, "dashboard/send.html")