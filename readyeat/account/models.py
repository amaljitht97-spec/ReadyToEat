from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
# Create your models here.

class User(AbstractUser):

    ROLE_CHOICES = (
        ("", "Choose Your Role"),
        ('donor', 'Donor'),
        ('customer', 'Customer'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.username
    
