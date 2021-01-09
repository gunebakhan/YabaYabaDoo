from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from django.utils import timezone
from .models import Product
# Create your views here.


class SingleProduct(DetailView):
    template_name = 'products/single-product.html'
    model = Product
    context_object_name = 'single_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ProductsList(ListView):
    model = Product
    template_name = 'products/products-list.html'
    ordering = ['-created']
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(category__slug=self.kwargs['slug'])

    
    def get_ordering(self):
        ordering = self.request.GET.get('ordering')
        # validate ordering here
        return ordering