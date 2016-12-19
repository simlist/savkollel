from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, FormView
from django.urls import reverse
from django.db import transaction
from django.db.models import Max
from django.http import HttpResponse

from nlaws.models import Product, Order, Invoice
from nlaws import utils
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
                                          product=Product.objects.get(pk=int(key)),
                                          quantity=quantity)
                        invoice.full_clean()
                        invoice.save()
                    
                return HttpResponse('Success')
        except:
            return HttpResponse(traceback.format_exc())


class Combine(LoginRequiredMixin, ListView):
    model = User
    
    def get(self, request, *args, **kwargs):
        try:
            orderdate = request.GET.get('orderdate')
            if orderdate is None:
                orderdate = date.today()
            else:
                orderdatelist = [int(n) for n in orderdate.split('-')]
                orderdate = date(*orderdatelist)
        
            orders = Order.objects.filter(order_date__gte=orderdate)
            maxdate = orders.aggregate(Max('order_date'))['order_date__max']
            orderdate = str(maxdate)
            actives = [order.customer.username for order in orders]
            users = [user.username for user in User.objects.all()]
            customers_status = {}
            for u in users:
                if u in actives:
                    customers_status[u] = {'status': 'Ready',
                                           'format' :'list-group-item-success'}
                else:
                    customers_status[u] = {'status': 'No list submitted',
                                           'format': 'list-group-item-danger'}
                                           
            context = {'customers_status': customers_status,
                       'orderdate': str(orderdate)}
            return render(request, r'nlaws/combine.html', context)
        
        except:
            return HttpResponse(traceback.format_exc())

    def post(self, request, *args, **qwargs):
        
        try:
            datelist = [int(n) for n in request.POST['orderdate'].split('-')]
            orderdate = date(*datelist)
            query = Invoice.objects.filter(order__order_date__gte=orderdate).values('product__name', 'quantity')
            dict = {}
            dicts = [{key['product__name']: key['quantity']} for key in query]
            combined_list = utils.merge_dicts(*dicts)
            
            context = {'orderdate': orderdate, 'combined_list': combined_list}
            
            return render(request, r'nlaws/invoice.html', context)
        except:
            return HttpResponse(traceback.format_exc())