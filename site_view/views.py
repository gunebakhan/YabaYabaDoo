from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from shop.models import ShopProduct
from products.models import Product, Category

# Create your views here.
class SliderView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["slides"] = Slider.objects.all()
        mobile_category = Category.objects.get(name="گوشی موبایل")
        mobile_phones = ShopProduct.objects.filter(product__category=mobile_category)
        context['mobiles'] = mobile_phones
        context['festival'] = Advertisement.objects.filter(status=True, priority='festival').first()
        context['highPriorityAdv'] = Advertisement.objects.filter(status=True, priority='high-adv')[:2]
        context['foursomeAdv'] = Advertisement.objects.filter(status=True, priority='foursome-adv')
        context['twosomeAdv'] = Advertisement.objects.filter(status=True, priority='twosome-adv')
        laptop_category = Category.objects.get(name='لپ تاپ')
        laptops = ShopProduct.objects.filter(product__category=laptop_category)
        context['laptops'] = laptops
        context['logos'] = Logo.objects.get(title='logo')
        return context


class FooterView(TemplateView):
    template_name = 'base/footer.html'
    model = Logo
    template_name = "logos"
    
