from django.contrib import admin

# Register your models here.
from .models import Produce, Customer

admin.site.register((Produce, Customer))