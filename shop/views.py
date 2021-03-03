from typing import List
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from shop.models import OrderItem, Shop, ShopProduct
from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm
from shop import cart
from django.views.generic import DetailView
from .tasks import order_created
from shop import forms



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
        return context
    
