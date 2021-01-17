from django.urls import path, include
from .views import SingleProduct, ProductsList


app_name = 'products'

urlpatterns = [
    path('product/<slug:slug>/', SingleProduct.as_view(), name='single_product'),
    path('categories/<slug:cat>/',
         ProductsList.as_view(), name='products_list'),
    path('categories/<slug:cat>/<slug:brand>/', ProductsList.as_view(), name='products_list_brands'),
]
