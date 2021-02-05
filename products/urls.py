from django.urls import path, include
from .views import ProductsList, LaptopDetail, MobileView, like_comment


app_name = 'products'

urlpatterns = [
    path('mobile-phone/<slug:slug>/', MobileView.as_view(), name='mobile_view'),
    path('laptop/<slug:slug>/', LaptopDetail.as_view(), name='laptop_view'),
    path('categories/<slug:cat>/',
         ProductsList.as_view(), name='products_list'),
    path('categories/<slug:cat>/<slug:brand>/', ProductsList.as_view(), name='products_list_brands'),
    path('like/', like_comment, name='like_comment'),
]
