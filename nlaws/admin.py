from django.contrib import admin

# Register your models here.
from .models import *

models = [Product, Order, Invoice]
admin.site.register(models)