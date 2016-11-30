from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)


class Order(models.Model):
    order_date = models.DateField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    produce = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

