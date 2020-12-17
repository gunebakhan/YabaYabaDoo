from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

# Create your models here.
class Shop(models.Model):

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_query_name='shop', related_name='shop', db_index=True)
    name = models.CharField(_("Name"), max_length=250, unique=True, db_index=True)
    slug = models.SlugField(_("Slug"), unique=True)
    discription = models.TextField(_("Discription"))
    image = models.ImageField(_("Image"), upload_to='shop/shops')
    joined = models.DateTimeField(_("Joined"), auto_now=False, auto_now_add=True)
    status = models.BooleanField(_("Status"), default=True)
    closed = models.BooleanField(_("Closed"), default=True)

    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")

    def __str__(self):
        return self.name


class ShopProduct(models.Model):

    shop = models.ForeignKey(Shop, verbose_name=_(""), on_delete=models.CASCADE, related_name='shop_product', related_query_name='shop_product')
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_name='shop_product', related_query_name='shop_product')
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    quantity = models.IntegerField(_("Quantity"))
    created = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("ShopProduct")
        verbose_name_plural = _("ShopProducts")

    def __str__(self):
        return self.product + ' ' + self.shop


