
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.db import models
from base.models import *
# Create your models here.


class Cart(models.Model):
    user = models.OneToOneField(
        Profile, on_delete=models.CASCADE, default=None)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return self.user.user.username + ' ' + str('cart') + ' ' + str(self.total_price)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.product.product_name
