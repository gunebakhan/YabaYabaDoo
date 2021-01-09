from django.urls import path, include
from .views import SingleProduct, ProductsList


app_name = 'products'

urlpatterns = [
    path('product/<slug:slug>/', SingleProduct.as_view(), name='single_product'),
    path('categories/<slug:slug>/', ProductsList.as_view(), name='products_list'),
]