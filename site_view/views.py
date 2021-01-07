from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from products.models import Product

# Create your views here.
class SliderView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["slides"] = Slider.objects.all()
        context['mobiles'] = Product.objects.filter(category__name="mobile")
        return context
    