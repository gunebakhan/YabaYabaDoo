# from django.db import models
# from django.utils.translation import ugettext_lazy as _
# from django.urls import reverse
# from shop.models import Shop


# # Create your models here.
# class Festival(models.Model):

#     name = models.CharField(_("Festival"), max_length=250)
#     image = models.ImageField(_("Image"), upload_to="home/festivals")

#     class Meta:
#         verbose_name = _("Festival")
#         verbose_name_plural = _("Festivals")

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse("Festival_detail", kwargs={"pk": self.pk})



# class Slider(models.Model):

#     lists = models.URLField(_("Lists"), max_length=200)
#     image = models.ImageField(_("Image"), upload_to="home/shops", height_field=None, width_field=None, max_length=None)



#     class Meta:
#         verbose_name = _("Slider")
#         verbose_name_plural = _("Sliders")

#     def __str__(self):
#         return self.shop

#     def get_absolute_url(self):
#         return reverse("Slider_detail", kwargs={"pk": self.pk})


# class ShopAdv(models.Model):

#     shop = models.ForeignKey(Shop, verbose_name=_("Shop"), on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = _("ShopAdv")
#         verbose_name_plural = _("ShopAdvs")

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse("ShopAdv_detail", kwargs={"pk": self.pk})
