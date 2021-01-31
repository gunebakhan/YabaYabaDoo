from django.urls import path
from . import views
from django.views.generic import TemplateView


app_names = "Users"

urlpatterns = [
    path('register/', views.SignUpView.as_view(), name='register'),
    path('activate/<slug:uidb64>/<slug:token>/',
         views.activate, name='activation'),
]
