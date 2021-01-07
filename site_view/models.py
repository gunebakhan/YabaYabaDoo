from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from shop.models import Shop


# Create your models here.
class Festival(models.Model):

    title = models.CharField(_("Title"), max_length=250)
    subtitle = models.CharField(_("Subtitle"), max_length=250)
    image = models.ImageField(_("Image"), upload_to="home/festival")

    class Meta:
        verbose_name = _("Festival")
        verbose_name_plural = _("Festivals")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Festival_detail", kwargs={"pk": self.pk})



class Slider(models.Model):

    title = models.CharField(_("Title"), max_length=250)
    subtitle = models.CharField(_("Subtitle"), max_length=250)
    # lists = models.URLField(_("Lists"), max_length=200)
    image = models.ImageField(_("Image"), upload_to="home/shops")
    action_url = models.URLField(_("Action Url"), max_length=200, default='http://127.0.0.1:8000')


    class Meta:
        verbose_name = _("Slider")
        verbose_name_plural = _("Sliders")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Slider_detail", kwargs={"pk": self.pk})


# class ShopAdv(models.Model):

#     shop = models.ForeignKey(Shop, verbose_name=_("Shop"), on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = _("ShopAdv")
#         verbose_name_plural = _("ShopAdvs")

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse("ShopAdv_detail", kwargs={"pk": self.pk})
