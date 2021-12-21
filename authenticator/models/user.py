from django.db import models
from django.db.models.deletion import CASCADE
from .role import Role

class User(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    verified_email = models.EmailField
    password = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True)
    last_login = models.DateTimeField
    password_update = models.DateField
    role = models.ForeignKey(Role, on_delete=CASCADE)