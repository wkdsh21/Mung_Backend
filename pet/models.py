from django.db import models
from django.conf import settings

# Create your models here.

class Pets(models.Model):
    pet_id = models.IntegerField()
    name = models.CharField(max_length=50)
    profile_img = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    species = models.CharField(max_length=50)
    is_neutering = models.BooleanField()
    birth_date = models.DateField()
    weight = models.FloatField()
    need_diet = models.BooleanField()
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class PetsWeights(models.Model):
    weight = models.FloatField()
    last_modified_at = models.DateTimeField(auto_now=True)
    pet = models.ForeignKey(Pets, on_delete=models.CASCADE)
