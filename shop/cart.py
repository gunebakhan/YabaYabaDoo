from django.conf import settings
from .models import ShopProduct
from decimal import Decimal
import redis


class Cart:
    def __init__(self, request) -> None:
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over items in the cart and get the products from the database.
        """
        shop_product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        shop_products = ShopProduct.objects.filter(id__in=shop_product_ids)

        cart = self.cart.copy()

        for product in shop_products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())



##################################### REDIS ############################################
# class RedisCard:
#     def __init__(self, request=None) -> None:
#         """
#         Initialize the cart.
#         """
#         if request is not None:
#             self.user_id = request.user.id
#         else: 
#             self.user_id = 1
#         self.redis = redis.Redis('127.0.0.1')
#         self.redis.set(self.user_id, {})

#     def add(self, product, quantity=1, override_quantity=False):
#         """
#         Add a product to the cart or update its quantity.
#         """
#         product_id = str(product.id)
#         if product_id not in self.redis.get(self.user_id):
#             self.redis.get(self.user_id)[product_id] = {
#                 'quantity': 0, 'price': str(product.price)}
        
#         if override_quantity:
#             self.redis.get(self.user_id)[product_id]['quantity'] = quantity
#         else:
#             self.redis.get(self.user_id)[product_id]['quantity'] = quantity
        
#     def remove(self, product):
#         """
#         Remove a product from redis
#         """
#         product_id = str(product.id)
#         if product_id in self.redis.get(self.user_id):
#             del self.redis.get(self.user_id)[product_id]
    
#     def clear(self):
#         # remove users cart
#         self.redis.delete(self.user_id)
    
#     def get_total_price(self):
#         total = 0
        
#         products = self.redis.get(self.user_id)

#         for product in products:
#             total += products[product]['price'] * products[product]['quantity']
        
#         return total


# class Product:
#     def __init__(self, id, price) -> None:
#         self.id = id
#         self.price = price

# product = Product(10, 399.99)

# cart = RedisCard()

# cart.add(product, quantity=1, override_quantity=False)
