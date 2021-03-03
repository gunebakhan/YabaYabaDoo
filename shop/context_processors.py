from .cart import Cart
from shop.models import Shop


def cart(request):
    return {'cart': Cart(request)}

def shops(request):
    shops = Shop.objects.all()
    return {'allshops': shops}