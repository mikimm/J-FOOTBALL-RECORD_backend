from django.db import models
from django.contrib.auth.models import AbstractUser,Group, Permission

class Gender(models.IntegerChoices):
        MAN = 1
        WOMAN = 2
        
class Users(AbstractUser):
    first_name = None
    last_name = None
    gender = models.IntegerField(choices=Gender)
