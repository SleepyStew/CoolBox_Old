from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.


class User(AbstractBaseUser):
    id = models.CharField(max_length=64, primary_key=True)
    cookie = models.CharField(max_length=64)
    name = models.CharField(max_length=128, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    required_fields = ['id', 'cookie', 'name']

    USERNAME_FIELD = 'name'

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name