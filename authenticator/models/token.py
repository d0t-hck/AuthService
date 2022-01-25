from django.db import models
from django.db.models.deletion import CASCADE
from .user import User


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, primary_key=True)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
