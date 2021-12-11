from django.db import models
from django.db.models.fields import DateTimeField

from base.models import Product, Profile
# Create your models here.
import datetime

#  now = datetime.datetime.now()


class Order(models.Model):
    sold_by = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="seller")
    bought_by = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="buyer")
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    time = models.DateTimeField(default=datetime.datetime.now(), blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.product.product_name + ' ' + str("Order")
