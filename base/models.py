from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import EmailField
from django.contrib.auth.models import AbstractUser
from PIL import Image
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    created_by = models.ForeignKey(
        Profile, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    descripton = models.TextField(null=True, blank=True)
    product_name = models.TextField(null=True, blank=True)
    price_in_rupees = models.IntegerField(default=0)

    def __str__(self):
        return str(self.product_name)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, default=None, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='product/images')

    def __str__(self):
        return self.product.product_name
