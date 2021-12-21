from django.db import models
from django.db.models.deletion import CASCADE
from .user import User

class Token(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)