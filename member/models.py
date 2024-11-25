from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    PROFILE_IMG_CHOICES = [
        ("0", "default"),
        ("1", "first"),
        ("2", "second"),
        ("3", "third"),
        ("4", "fourth"),
        ("5", "fifth"),
        ("6", "sixth"),
    ]
    user_img = models.CharField(max_length=10, choices=PROFILE_IMG_CHOICES, default="0")
    pet_cnt = models.IntegerField("pet_count", default=0)
