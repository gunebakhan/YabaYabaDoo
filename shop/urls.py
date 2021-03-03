from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('order_create/', views.order_create, name='order_create'),
    path('create_shop_product/<slug:shop>/', views.Create_Shop_Product.as_view(), name='create_shop_product'),
    path('shop/<slug:slug>/', views.ShopDetail.as_view(), name='shop_detail'),
    path('<int:pk>/', views.EditShopProductView.as_view(), name='edit_shop_product'),
    path('', views.cart_detail, name='cart_detail'),
]
