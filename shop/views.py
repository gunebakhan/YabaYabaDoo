from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import ShopProduct
from .cart import Cart
from .forms import CartAddProductForm
from shop import cart
from django.views.generic import DetailView

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



    
