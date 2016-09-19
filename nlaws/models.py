from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100)

class Produce(models.Model):
    product = models.CharField(max_length=100)

class Order(models.Model):
    order_date = models.DateField()
    customer = models.ForeignKey(Customer)
    produce = models.ForeignKey(Produce)
    quantity = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
