from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from shop.models import Shop


# Create your models here.
class Advertisement(models.Model):
    options = (
        ('festival', 'Festival'),
        ('high-adv', 'High Priority Advertisement'),
        ('foursome-adv', 'Foursom Advertisement'),
        ('twosome-adv', 'Twosome Advertisement')

    )
    title = models.CharField(_("Title"), max_length=250)
    subtitle = models.CharField(_("Subtitle"), max_length=250)
    image = models.ImageField(_("Image"), upload_to="home/festival")
    priority = models.CharField(_("Priority"), max_length=50, choices=options)
    status = models.BooleanField(_("Status"), default=False)
    url = models.URLField(_("Url"), max_length=200,
                          default="https://google.com")

    class Meta:
        verbose_name = _("Advertisement")
        verbose_name_plural = _("Advertisements")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Advertisement_detail", kwargs={"pk": self.pk})


class Slider(models.Model):

    title = models.CharField(_("Title"), max_length=250)
    subtitle = models.CharField(_("Subtitle"), max_length=250)
    status = models.BooleanField(_("Status"), default=True)
    image = models.ImageField(_("Image"), upload_to="home/shops")
    action_url = models.URLField(
        _("Action Url"), max_length=200, default='http://127.0.0.1:8000')

    class Meta:
        verbose_name = _("Slider")
        verbose_name_plural = _("Sliders")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Slider_detail", kwargs={"pk": self.pk})


class Logo(models.Model):

    title = models.CharField(_("Title"), max_length=250)
    subtitle = models.CharField(_("Subtitle"), max_length=250)
    # lists = models.URLField(_("Lists"), max_length=200)
    image = models.ImageField(_("Image"), upload_to="home/shops")

    class Meta:
        verbose_name = _("Logo")
        verbose_name_plural = _("Logos")

    def __str__(self):
        return self.subtitle

    def get_absolute_url(self):
        return reverse("Logo_detail", kwargs={"pk": self.pk})


# class ShopAdv(models.Model):

#     shop = models.ForeignKey(Shop, verbose_name=_("Shop"), on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = _("ShopAdv")
#         verbose_name_plural = _("ShopAdvs")

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse("ShopAdv_detail", kwargs={"pk": self.pk})
