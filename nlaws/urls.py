from django.conf.urls import url
from .views import *

app_name = 'nlaws'
urlpatterns = [url(r'^$', index, name='index'),
               url(r'^shoppinglist$', ShoppingList.as_view(), name='shoppinglist'),
               url(r'^combine$', Combine.as_view(), name='combine'),
               url(r'^viewlist$', ViewList.as_view(), name='viewlist'),
               url(r'^orderslist$', ViewOrders.as_view(), name='orderslist'),
               url(r'^deleteorder$', DeleteOrder.as_view(), name='deleteorder'),
               url(r'^addproduct$', AddProduct.as_view(), name='addproduct'),
               url(r'^checklist/(?P<order_id>[0-9]+)$',
                   Checklist.as_view(),
                   name='checklist'),
               ]
