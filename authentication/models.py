from django.db import models
from django.contrib.auth.models import User
from helpers import random_str

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)


class AuthenticationRequest(models.Model):
    code = models.CharField(max_length=30, default=random_str(30, alpha=True), unique=True)
