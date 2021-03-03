from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('order_create/', views.order_create, name='order_create'),
    path('shop/<slug:slug>/', views.ShopDetail.as_view(), name='shop_detail'),
]
