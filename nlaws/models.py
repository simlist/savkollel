from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100)

class Produce(models.Model):
    product = CharField(max_length=100)

class Order(models.Model):
    order_date = models.DateField()
    customer = ForeignKey(Customer)
    produce = ForeignKey(Produce)
    quantity = IntegerField()

