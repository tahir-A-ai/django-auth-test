from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=16, default='', blank=True)
    address = models.TextField(blank=True, null=True)
    profile_image = CloudinaryField('image', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username']

    def __str__(self):
        return self.email


class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.IntegerField(default=0)
    currency = models.CharField(max_length=20, default="Gems")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet: {self.balance} {self.currency}"