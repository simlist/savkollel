from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, FormView
from django.urls import reverse
from django.db import transaction
from django.http import HttpResponse

from nlaws.models import Product, Order, Invoice
#debug
import traceback


# Create your views here.
@login_required
def index(request):
    return render(request, r'nlaws/index.html')


class ShoppingList(LoginRequiredMixin, ListView):

    model = Product

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        data = request.POST.copy()
        pickupdate = [int(n) for n in data.pop('pickupdate')[0].split('-')]


        data.pop('csrfmiddlewaretoken')

        try:
            with transaction.atomic():
                pickupdate = date(*pickupdate)
                order = Order(order_date=pickupdate, customer=request.user)
                order.full_clean()
                order.save()
                for key in data:
                    quantity = int(data[key])
                    if quantity:
                        invoice = Invoice(order=order,
                                          produce=Product.objects.get(pk=int(key)),
                                          quantity=quantity)
                        invoice.full_clean()
                        invoice.save()
                    
                return HttpResponse('Success')
        except:
            return HttpResponse(traceback.format_exc())


class Combine(LoginRequiredMixin, ListView):
    model = User
    
    def get(self, request, *args, **kwargs):
        orderdate = request.GET.get('orderdate')
        if orderdate is None:
            orderdate = date.today()
        else:
            orderdatelist = [int(n) for n in orderdate.split('-')]
            orderdate = date(*orderdatelist)
        
        orders = Order.objects.filter(orderdate__gte=orderdate)
        actives = [order.customer.username for order in orders]
        users = [user.username for user in User.objects.all()]
        context = {'actives': actives, 'users': users}

        return render(request, r'nlaws/combine.html', context)


