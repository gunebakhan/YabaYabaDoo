from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from products.models import Product
from django.utils import timezone
User = get_user_model()

# Create your models here.
class Shop(models.Model):

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_query_name='shop', related_name='shop', db_index=True)
    name = models.CharField(_("Name"), max_length=250, unique=True, db_index=True)
    slug = models.SlugField(_("Slug"), unique=True)
    discription = models.TextField(_("Discription"))
    image = models.ImageField(_("Image"), upload_to='shop/shops')
    shop_product = models.ManyToManyField(Product, verbose_name=_("Shop Product"), through='ShopProduct', related_name='shops')
    joined = models.DateTimeField(_("Joined"), auto_now=False, auto_now_add=True)
    status = models.BooleanField(_("Status"), default=True)
    closed = models.BooleanField(_("Closed"), default=True)

    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")

    def __str__(self):
        return self.name


class ShopProduct(models.Model):

    shop = models.ForeignKey(Shop, verbose_name=_("Shop"), on_delete=models.CASCADE, related_name='shop_products', related_query_name='shop_products')
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_name='shop_products', related_query_name='shop_products')
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    quantity = models.IntegerField(_("Quantity"))
    created = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("ShopProduct")
        verbose_name_plural = _("ShopProducts")

    def __str__(self):
        return self.product.name 
    

class OrderItem(models.Model):

    order = models.ForeignKey("Order", verbose_name=_("Order"), on_delete=models.CASCADE, related_query_name='order_items', related_name='order_items')
    shop_product = models.ForeignKey(ShopProduct, verbose_name=_("Shop Product"), on_delete=models.CASCADE, related_query_name='order_items', related_name='order_items')
    count = models.IntegerField(_("Counts"))
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(_("Create At"), auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(_("Update At"), auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("OrderItem")
        verbose_name_plural = _("OrderItems")

    def __str__(self):
        return self.shop_product.product.name


class Order(models.Model):

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_query_name='orders', related_name='orders')
    create_at = models.DateTimeField(_("Create At"), auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(_("Update At"), auto_now=True, auto_now_add=False)
    discription = models.TextField(_("Discription"))
    paid = models.BooleanField(_("Paid"), default=False)


    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return self.discription
    
    @property
    def total_order_price(self):
        order_items = self.order_items.all()
        
        total_price = 0.0
        for item in order_items:
            total_price += (item.count * item.price)
        
        return total_price



class Payment(models.Model):

    order = models.OneToOneField(Order, verbose_name=_("Order"), on_delete=models.CASCADE, related_query_name='payments', related_name="payments")
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_query_name='payments', related_name='payments')
    paid_price = models.DecimalField(_("Paid Price"), max_digits=10, decimal_places=2, default=0.0)
    create_at = models.DateTimeField(_("Create At"), auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(_("Update At"), auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self):
        return self.order + " " + self.user
    
    def pay_the_price(self):
        self.paid_price = self.order.total_order_price


class BasketItem(models.Model):

    basket = models.ForeignKey("Basket", verbose_name=_("Basket"), on_delete=models.CASCADE, related_query_name='basket_items', related_name='basket_items')
    shop_product = models.ForeignKey(ShopProduct, verbose_name=_("Shop Product"), on_delete=models.CASCADE, related_query_name='basket_items', related_name='basket_items')
    count = models.IntegerField(_("Count"))
    create_at = models.DateTimeField(_("Create At"), auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(_("Update At"), auto_now=True, auto_now_add=False)


    class Meta:
        verbose_name = _("BasketItem")
        verbose_name_plural = _("BasketItems")

    def __str__(self):
        return f"{self.shop_product} in {self.basket}"



class Basket(models.Model):

    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE, related_query_name='baskets', related_name='baskets')

    create_at = models.DateTimeField(_("Create At"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update At"), auto_now=True)

    class Meta:
        verbose_name = _("Basket")
        verbose_name_plural = _("Baskets")

    def __str__(self):
        return f"{self.user}'s Basket"
    
    @property
    def basket_price(self):
        basket_items = Basket.basket_items.all()

        total_price = 0.0
        
        for item in basket_items:
            total_price += (item.shop_product.price * item.count)
        
        return total_price
        
