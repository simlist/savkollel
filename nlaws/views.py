from datetime import date
import urllib
from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.views import View
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


class ShoppingList(LoginRequiredMixin, View):
    """Create an order."""

    def get(self, request, *args, **kwargs):
        saved_dict = {}
        orderdate = ''
        order_id = ''
        if request.GET:
            saved_dict = request.GET.copy()
            order_id = saved_dict.pop('order', [None,])[0]
            orderdate = saved_dict.pop('orderdate', ['',])[0]
            saved_dict = {urllib.unquote(n): int(saved_dict[n][0]) for n in saved_dict}  #dict comprehension

        products = Product.objects.all()
        invoice = [{'product': product, 'quantity': saved_dict.get(product.name, '')}
                   for product in products]
        context = {'orderdate': orderdate, 'invoice': invoice,
                   'order': order_id}
        return render(request, 'nlaws/product_list.html', context)


    @transaction.atomic
    def post(self, request, *args, **kwargs):

        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken')
        pickupdate = utils.date_from_string(data.pop('pickupdate')[0])

        try:
            with transaction.atomic():
                order_id = data.pop('order', '')
                if order_id:
                    order = Order.objects.get(pk=int(order_id[0]))
                    order.order_date = pickupdate
                    Invoice.objects.filter(order=order).delete()
                else:
                    order = Order(order_date=pickupdate, customer=request.user)
                order.full_clean()
                order.save()

                for key in data:
                    quantity = data[key]
                    if quantity and int(quantity):
                        invoice = Invoice(order=order,
                                          product=Product.objects.get(pk=int(key)),
                                          quantity=int(quantity))
                        invoice.full_clean()
                        invoice.save()

                return render(request, 'nlaws/index.html', {'text': 'success'})
        except:
            return HttpResponse(traceback.format_exc())


class Combine(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        try:
            today = date.today()
            orders = Order.objects.filter(order_date__gte=today)
            maxdate = str(orders.aggregate(Max('order_date'))['order_date__max'])
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
                       'maxdate': maxdate}
            return render(request, r'nlaws/combine.html', context)

        except:
            return HttpResponse(traceback.format_exc())

    def post(self, request, *args, **qwargs):

        orderdate = utils.date_from_string(request.POST['maxdate'])
        today = date.today()
        query = Invoice.objects.filter(order__order_date__gte=today)
        dicts = [{line.product: line.quantity} for line in query]
        combined_list = utils.merge_dicts(*dicts)
        invoice_list = [{'product': key, 'quantity': combined_list[key]}
                        for key in combined_list]
        invoice_list.sort(key=lambda e: e['product'].name)
        context = {'orderdate': orderdate, 'invoice_list': invoice_list,
                   'title': 'Combined order', 'sender': 'Combine'}

        return render(request, r'nlaws/invoice.html', context)


class ViewList(LoginRequiredMixin, View):
    """View a single order."""

    def get(self, request, *args, **qwargs):
        order_id = request.GET['order']
        query = Invoice.objects.filter(order__pk=order_id,
                                       order__customer=request.user)
        orderdate = query.aggregate(Max('order__order_date'))['order__order_date__max']
        username = request.user.username
        context = {'invoice_list': query, 'orderdate': orderdate,
                   'title': "{0}'s order ".format(username),
                   'order_id': order_id,'editable': True}
        return render(request, 'nlaws/invoice.html', context)


class ViewOrders(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        query = Order.objects.filter(customer=request.user)
        orderlist = [{'date': str(q.order_date), 'id': str(q.pk)} for q in query]
        context = {'orderlist': orderlist}
        return render(request, 'nlaws/orderslist.html', context)

class DeleteOrder(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        key = int(request.GET['order'])
        order = Order.objects.filter(customer=request.user,
                                     pk=key)
        order.delete()
        return redirect('/nlaws/orderslist')


class AddProduct(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'nlaws/addproduct.html')

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        name=request.POST['productname']
        try:
            with transaction.atomic():
                product = Product(name=name)
                product.full_clean()
                product.save()
                return render(request, 'nlaws/index.html', {'text': 'Success!'})
        except:
            return render(request, 'nlaws/index.html', {'text': 'There were errors'})


class Checklist(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order_list = get_list_or_404(Invoice, order__id=order_id)
        return render(
                      request, 'nlaws/checklist.html',
                      {'order_list': order_list, 'order_id': order_id}
                     )

    def post(self, request, order_id):
        post = request.POST
        order_invoice = list(Invoice.objects.filter(order__id=order_id))
        missing_list = []
        for line in order_invoice:
            if str(line.pk) in post:
                if line.quantity > int(post[str(line.pk)]):
                    line.quantity -= int(post[str(line.pk)])
                    missing_list.append(line)
            else:
                missing_list.append(line)
        context = {'missing_list': missing_list, 'order_id': order_id}
        return render(request, 'nlaws/checklist_result.html', context)
