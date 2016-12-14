from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse
from django.db import transaction
from django.http import HttpResponse

from nlaws.models import Product, Order, Invoice
#debug
import traceback


# Create your views here.
@login_required
def index(request):
    return render(request, 'nlaws/index.html')


class ShoppingList(LoginRequiredMixin, ListView):

    model = Product

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        data = request.POST.copy()
        pickupdate = data.pop('pickupdate')[0].split('-')

        data.pop('csrfmiddlewaretoken')

        try:
            with transaction.atomic():
                pickupdate = date(int(pickupdate[0]),
                                  int(pickupdate[1]),
                                  int(pickupdate[2]))
                order = Order(order_date=pickupdate, customer=request.user,status=True)
                order.full_clean()
                order.save()
                for key in data:
                    invoice = Invoice(order=order,
                                      produce=Product.objects.get(pk=int(key)),
                                      quantity=int(data[key]))
                    invoice.full_clean()
                    invoice.save()
                    
                return HttpResponse('Success')
        except:
            return HttpResponse(traceback.format_exc())