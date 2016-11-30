from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from nlaws.models import Product


# Create your views here.
@login_required
def index(request):
    return render(request, 'nlaws/index.html')


class ShoppingList(LoginRequiredMixin, ListView):

    model = Product
