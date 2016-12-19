from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Order(models.Model):
    order_date = models.DateField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{0} {1}'.format(str(self.order_date), str(self.customer))

    class Meta:
        ordering = ['-order_date']

class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return '{0}-{1} {2}'.format(str(self.order),
                                    str(self.quantity),
                                    str(self.product))

    class Meta:
        ordering = ['product']

