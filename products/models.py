from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Create your models here.
####################### Product Requirments ############################
class Category(models.Model):

    name = models.CharField(_("Name"), max_length=200, db_index=True)
    slug = models.SlugField(_("Slug"), max_length=200, unique=True)
    parent = models.ForeignKey("self", verbose_name=_("Parent"), on_delete=models.SET_NULL, null=True, blank=True, related_query_name='child', related_name='child')
    create = models.DateTimeField(_("Create"), auto_now=False, auto_now_add=True)
    update = models.DateTimeField(_("Update"), auto_now=True, auto_now_add=False)
    details = models.TextField(_("Details"))
    image = models.ImageField(_("Image"), upload_to='products/categpry')

    class Meta:
        ordering = ('name',)
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Brand(models.Model):

    name = models.CharField(_("Name"), max_length=50, db_index=True)
    slug = models.SlugField(_("Slug"), max_length=200, unique=True)
    create = models.DateTimeField(_("Create"), auto_now=False, auto_now_add=True)
    update = models.DateTimeField(_("Update"), auto_now=True, auto_now_add=False)
    details = models.TextField(_("Details"))

    class Meta:
        ordering = ('name',)
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.name


class ImageGallery(models.Model):

    image = models.ImageField(_("Image"), upload_to='media/products/images/%Y/%m/%d', blank=True)
    product = models.ForeignKey("Product", verbose_name=_("Product"), on_delete=models.CASCADE, related_name='image_gallery', related_query_name='image_gallery')
    created = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)   

    class Meta:
        verbose_name = _("ImageGallery")
        verbose_name_plural = _("ImageGalleries")

    def __str__(self):
        return self.product




class Product(models.Model):

    category = models.ForeignKey(Category, verbose_name=_("Category"), on_delete=models.CASCADE, related_name='product', related_query_name='product')
    brand = models.ForeignKey(Brand, verbose_name=_("Brand"), on_delete=models.CASCADE, related_name='product', related_query_name='product')
    name = models.CharField(_("Name"), max_length=200, db_index=True)
    slug = models.SlugField(_("Slug"), max_length=200, db_index=True)
    description = models.TextField(_("Description"), blank=True)
    image = models.ImageField(_("Image"), upload_to='media/products')
    created = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)


    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name


class ProductMeta(models.Model):

    product = models.ForeignKey(Product, verbose_name=_("product"), on_delete=models.CASCADE, related_name='meta', related_query_name='meta')
    label = models.CharField(_("Label"), max_length=250)
    value = models.CharField(_("Value"), max_length=250)
    created = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("ProductMeta")
        verbose_name_plural = _("ProductMetas")

    def __str__(self):
        return self.label



class Comment(models.Model):

    RATING_CHOICES = (
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Foure'),
        (5, 'Five'),
    )
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE, related_query_name='comment', related_name='comment')
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_name='comment', related_query_name='comment')
    title = models.CharField(_("Title"), max_length=250, db_index=True)
    body = models.TextField(_("Body"))
    rate = models.CharField(_("Rate"), max_length=50, choices=RATING_CHOICES)
    created = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)
    publish = models.DateTimeField(_("Publish"), default=timezone.now)
    draft = models.BooleanField(_("Draft"), default=False)

    
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.title


class LikeProduct(models.Model):

    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_query_name='likes', related_name='likes')
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_query_name='likes', related_name='likes')
    condition = models.BinaryField(_("Condition"), blank=True, null=True)

    class Meta:
        verbose_name = _("LikeProduct")
        verbose_name_plural = _("LikeProducts")

    def __str__(self):
        return f"{self.user}-{self.product}"

