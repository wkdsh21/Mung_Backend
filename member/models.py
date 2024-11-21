from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_img = models.CharField(max_length=50, blank=True)