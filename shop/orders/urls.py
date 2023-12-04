from django.urls import path

from orders.views import BuyView, ItemView, OrderView

app_name = 'orders'


urlpatterns = [
    path('buy/<int:item_id>/', BuyView.as_view(), name='buy'),
    path('item/<int:item_id>/', ItemView.as_view(), name='item'),
    path('order/<int:order_id>/', OrderView.as_view(), name='order'),
]
