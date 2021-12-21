from django.db import models
from django.db.models.deletion import CASCADE
from .user import User

class Code(models.Model):
    code = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField
    is_used = models.BooleanField(default=False)
