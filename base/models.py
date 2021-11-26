from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import EmailField

# Create your models here.


class buyer(models.Model):
    name = models.CharField(max_length=20)
    phonenumber = models.CharField(max_length=10)
    department = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(
        User, related_name='buyer', on_delete=models.CASCADE)
