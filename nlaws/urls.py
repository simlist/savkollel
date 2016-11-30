from django.conf.urls import url
from .views import *

app_name = 'nlaws'
urlpatterns = [url(r'^$', index, name='index'),
               url(r'^shoppinglist$', ShoppingList.as_view(), name='shoppinglist')
               ]