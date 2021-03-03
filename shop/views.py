from typing import List
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from shop.models import OrderItem, Shop, ShopProduct
from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm, ShopProductForm
from shop import cart
from django.views.generic import DetailView, UpdateView, CreateView
from .tasks import order_created
from shop import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import Product
from django.urls import reverse, reverse_lazy

# Create your views here.
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ShopProduct, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('shop:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ShopProduct, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'override': True})
    return render(request, 'cart/detail.html', {'cart': cart})


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            # print('dsrrf')
            # print(request.user.id)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         shop_product=item['product'],
                                         price=item['price'],
                                         count=item['quantity'])
            # clear cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            return render(request, 'orders/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})


class ShopDetail(DetailView):
    model = Shop
    template_name = 'shop/shop_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = ShopProduct.objects.filter(shop=self.object)
        context['owner'] = self.object.user
        return context
    

class EditShopProductView(LoginRequiredMixin, UpdateView):
    template_name = "shop/edit_shop_product.html"
    model = ShopProduct
    form_class = ShopProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = Product.objects.get(shop_products=self.object)
        return context
    
    def get_success_url(self, *args, **kwargs):
        return reverse("shop:shop_detail", kwargs={'slug': self.object.shop.slug})
    

class Create_Shop_Product(LoginRequiredMixin, CreateView):
    form_class = forms.CreateShopProductForm
    template_name = 'shop/create_shop_product.html'
    
    def form_valid(self, form):
        form = form.save(commit=False)
        form.shop = Shop.objects.get(slug=self.kwargs.get('shop'))
        form.save()
        
        return super().form_valid(form)


    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return render(self.request, 'shop/create_shop_product.html', {"form": self.get_form()})
        

    def get_success_url(self):
        return reverse("shop:shop_detail", kwargs={
            'slug': self.kwargs.get('shop')})
