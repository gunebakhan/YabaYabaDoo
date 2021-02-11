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


DEFAULT_CAT_ID = 1
class Brand(models.Model):

    name = models.CharField(_("Name"), max_length=50, db_index=True)
    slug = models.SlugField(_("Slug"), max_length=200, unique=True)
    product_type = models.ForeignKey("Category", verbose_name=_(
        "Product Type"), on_delete=models.CASCADE, blank=True, null=True)
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
        return self.product.name




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
    size = models.CharField(_("Height Width Length"), max_length=50, default="None")
    weight = models.CharField(_("Weight"), max_length=50, default="None")
    cpu_manufacturer = models.CharField(_("CPU Manufacturer"), max_length=50, default="None")
    cpu_series = models.CharField(_("CPU Series"), max_length=50, default="None")
    cpu_model = models.CharField(_("CPU Model"), max_length=50, default="None")
    cpu_speed = models.CharField(_("CPU Speed"), max_length=50, default="None")
    cach = models.CharField(_("Cach"), max_length=50, default="0")
    ram_capacity = models.CharField(_("RAM Capacity"), max_length=50, default="None")
    ram_type = models.CharField(_("RAM Type"), max_length=50, default="None")
    storage = models.CharField(_("Storage"), max_length=50, default="None")
    storage_type = models.CharField(_("Storage Type"), max_length=50, default="None")
    gpu_manufacturer = models.CharField(_("GPU Manufacturer"), max_length=50, default="None")
    gpu_model = models.CharField(_("GPU Model"), max_length=50, default="None")
    gpu_ram = models.CharField(_("GPU RAM"), max_length=50, default="None")
    display_size = models.CharField(_("Display Size"), max_length=50, default='None')
    display_type = models.CharField(_("Display Type"), max_length=50, default="None")
    display_accuracy = models.CharField(_("Display Accuracy"), max_length=50, default="None")
    display_mate = models.BooleanField(_("Display Mate"), default=False)
    display_touchable = models.BooleanField(_("Display Touchable"), default=False)
    created = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("ProductMeta")
        verbose_name_plural = _("ProductMetas")

    def __str__(self):
        return self.product.name


class MobileMeta(models.Model):
    SLOT_CHOICES = (
        (('دارد'), ('دارد')),
        (('ندارد'), ('ندارد')),
    )

    YES_NO_CHOICES = (
        (('بلی'), ('بلی')),
        (('خیر'), ('خیر')),
    )
    product = models.ForeignKey(Product, verbose_name=_(
        "product"), on_delete=models.CASCADE, related_name='mobile_meta', related_query_name='mobile_meta')

    size = models.CharField(_("Size"), max_length=50)
    sim_card_desc = models.CharField(_("Sim Card Descrioption"), max_length=50)
    weight = models.CharField(_("Weight"), max_length=50)
    body_structure = models.CharField(_("Body Structur"), max_length=50)
    special_properties = models.CharField(_("Special Properties"), max_length=50)
    num_sim_cards = models.CharField(_("Num of Sim Cards"), max_length=50)
    intro_date = models.DateTimeField(_("Introduction Date"), auto_now=False, auto_now_add=False)
    slot_for_sim = models.CharField(_("Slot For Sim"), max_length=50, choices=SLOT_CHOICES)
    model = models.CharField(_("Model"), max_length=50)
    cpu_chipset = models.CharField(_("CPU Chipset"), max_length=250)
    cpu = models.CharField(_("CPU"), max_length=250)
    cpu_type = models.CharField(_("CPU Type"), max_length=50)
    cpu_freequency = models.CharField(_("CPU Frequency"), max_length=50)
    gpu = models.CharField(_("GPU"), max_length=50)
    ram = models.CharField(_("RAM"), max_length=50)
    ram_capacity = models.CharField(_("RAM Capacity"), max_length=50)
    side_storage = models.CharField(_("Side Storage"), max_length=50)
    side_storage_standard = models.CharField(_("Side Storage Standard"), max_length=50)
    colorful_display = models.CharField(_("Colorful Storage"), max_length=50, choices=YES_NO_CHOICES)
    touchable_display = models.CharField(_("Touchable Display"), max_length=50, choices=YES_NO_CHOICES)
    display_techno = models.CharField(_("Display Techni"), max_length=50)
    display_size_range = models.CharField(_("Display Size Range"), max_length=50)
    display_size = models.CharField(_("Display Size"), max_length=50)
    resolution = models.CharField(_("Resolution"), max_length=50)
    pixel_density = models.CharField(_("Pixel Density"), max_length=50)
    display_to_body = models.CharField(_("Display to Body"), max_length=50)
    display_ratio = models.CharField(_("Display Ratio"), max_length=50)
    networks = models.CharField(_("Networks"), max_length=50)
    network_2g = models.CharField(_("2G Network"), max_length=250)
    network_3g = models.CharField(_("3G Network"), max_length=250)
    network_4g = models.CharField(_("4G Network"), max_length=250)
    connection_technology = models.CharField(_("Connection Technology"), max_length=250)
    wifi = models.CharField(_("Wi-Fi"), max_length=250)
    bluetooth = models.CharField(_("Bluetooth"), max_length=250)
    location_techno = models.CharField(_("Location Technology"), max_length=250)
    port = models.CharField(_("Port"), max_length=250)
    back_camera_modules = models.CharField(_("Back Camera Modules"), max_length=50)
    image_resolution = models.CharField(_("Image Resolution"), max_length=50)
    flash = models.CharField(_("Flash"), max_length=50)
    camera_capabalities = models.TextField(_("Camera Capabalities"))
    filming = models.CharField(_("Filming"), max_length=250)
    selfie_camera = models.CharField(_("Selfie Camera"), max_length=1024)
    speaker = models.CharField(_("Speaker"), max_length=50, choices=YES_NO_CHOICES)
    voice_output = models.CharField(_("Voice Output"), max_length=50)
    os = models.CharField(_("OS"), max_length=50)
    os_release = models.CharField(_("OS Realease"), max_length=50)
    software_capabalities = models.TextField(_("Software Capabalities"))
    created = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False, null=True, blank=True)


    class Meta:
        verbose_name = _("MobileMeta")
        verbose_name_plural = _("MobileMetas")

    def __str__(self):
        return self.product.name




class CommentLike(models.Model):

    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment", verbose_name=_("Comment"), on_delete=models.CASCADE)
    condition = models.BooleanField(_("Condition"))
    create_at = models.DateTimeField(_("Create at"), auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("CommentLike")
        verbose_name_plural = _("CommentLikes")

    def __str__(self):
        return self.condition



class Comment(models.Model):

    RATING_CHOICES = (
        (0, 'صفر'),
        (1, 'یک'),
        (2, 'دو'),
        (3, 'سه'),
        (4, 'چهار'),
        (5, 'پنج'),
    )
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE, related_query_name='comment', related_name='comment')
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_name='comment', related_query_name='comment')
    title = models.CharField(_("Title"), max_length=250, db_index=True)
    body = models.TextField(_("Body"))
    rate = models.IntegerField(_("Rate"), choices=RATING_CHOICES, default=0)
    created = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)
    publish = models.DateTimeField(_("Publish"), default=timezone.now)
    draft = models.BooleanField(_("Draft"), default=True)

    
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

