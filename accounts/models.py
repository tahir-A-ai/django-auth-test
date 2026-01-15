from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, default='')
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.email
