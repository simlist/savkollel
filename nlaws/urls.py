from django.conf.urls import url
from .views import *

app_name = 'nlaws'
urlpatterns = [url(r'^$', index, name='index'),
               url(r'^shoppinglist$', ShoppingList.as_view(), name='shoppinglist'),
               url(r'^combine$', Combine.as_view(), name='combine')
               ]