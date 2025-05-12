from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('item_remove/<int:pk>/', views.item_remove, name='item_remove'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('order/create/', views.order_create, name='order_create'),
    path('orders/', views.orders_list, name='orders'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/cancel/<int:pk>/', views.cancel_order, name='cancel_order'),
    path('order/<int:order_id>/pay/', views.create_payment, name='create_payment'),
    path('payment/success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('yookassa-webhook/', views.yookassa_webhook, name='yookassa_webhook'),
]