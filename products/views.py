from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from braces.views import JSONResponseMixin
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import ModelFormMixin, FormMixin
from django.utils import timezone
from .models import Product, Comment
from .forms import CommentForm
from django.views import View
import json
from django.contrib import messages


# Create your views here.
class AjaxableResponseMixin:
    def render_to_json_response(self, context, **response_kwargs):
        """Render a json response of context."""
        data = json.dumps(context)
        # data = serializers.serialize('json', context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)
    

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).from_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        return response
    
    def form_valid(self, form):
        form = form.save(commit=False)
        form.author = self.request.user
        form.product = Product.objects.get(slug=self.kwargs.get('slug'))
        form.save()
        if self.request.is_ajax():
            # Request is ajax, send a json response
            data = {
                'title': form.title,
                'body': form.body,
            }
            return self.render_to_json_response(data)
        return super().form_valid(form)


class LaptopAjaxView(JSONResponseMixin, DetailView):
    model = Product
    content_type = 'application/javascript'
    json_dumps_kwargs = {'indent': 2}
    template_name = 'products/single-product1.html'

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     context_dict = {
    #         'name': self.object.name,
    #         ''
    #     }

class LaptopDetail(AjaxableResponseMixin, FormMixin, DetailView):
    model = Product
    template_name = 'products/single-product1.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('products:laptop_view', kwargs={'slug': self.kwargs.get('slug')})
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['comments'] = Comment.objects.filter(draft=True, product=self.object)

        return context
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    
    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            print('ajax')
        else:
            print('salam')
            return super().get(request, *args, **kwargs)


# class LaptopDetail(FormMixin, DetailView):
#     model = Product
#     template_name = 'products/single-product1.html'
#     form_class = CommentForm

#     def get_success_url(self):
#         return reverse('products:laptop_view', kwargs={'slug': self.kwargs.get('slug')})

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['comments'] = Comment.objects.filter(draft=False)

#         return context

#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

#     def form_valid(self, form):
#         form = form.save(commit=False)
#         print(form)
#         form.author = self.request.user
        # print('slug', self.kwargs.get('slug'))
        # form.product = Product.objects.get(slug=self.kwargs.get('slug'))
        # form.save()
        # print(form)
        # return super().form_valid(form)

# Mobile Single View
class MobileView(DetailView):
    template_name = 'products/single-product1.html'
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
        if self.kwargs.get('brand') is not None:
            return qs.filter(category__slug=self.kwargs['cat'], brand__slug=self.kwargs['brand'])
        return qs.filter(category__slug=self.kwargs['cat'])

    
    def get_ordering(self):
        ordering = self.request.GET.get('ordering')

        if ordering == 'price':
            pass
        # validate ordering here
        return ordering
