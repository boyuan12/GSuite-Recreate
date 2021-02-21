from django.shortcuts import render
from .models import Email
from django.http import HttpResponse


# Create your views here.
def index(request):
    emails = Email.objects.filter(to_email=f"{request.user.username}@devwithme.xyz")
    return render(request, "dashboard/index.html", {
        "emails": emails
    })
