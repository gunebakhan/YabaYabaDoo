from django.urls import path, include
from .views import *

app_name = 'site_view'

urlpatterns = [
    path('', SliderView.as_view(), name='home'),
    # path('', include(''))
]