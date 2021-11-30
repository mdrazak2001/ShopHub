from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import EmailField
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    descripton = models.TextField(null=True, blank=True)
    product_name = models.TextField(null=True, blank=True)
    # type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to='product_photo', blank=True)
    price_in_rupees = models.IntegerField(default=0)

    def __str__(self):
        return str(self.product_name)
