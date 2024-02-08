from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    phone_number = models.CharField(null=False, max_length=15)
    email = models.EmailField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
