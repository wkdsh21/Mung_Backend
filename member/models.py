from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    user_img = models.CharField(max_length=50, blank=True)