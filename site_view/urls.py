from django.urls import path, include
from django.views.generic import TemplateView

app_name = 'site_view'

urlpatterns = [
    path('', TemplateView.as_view(template_name='home/index.html'), name='home'),
    # path('', include(''))
]