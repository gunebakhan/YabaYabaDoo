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
        context["slides"] = Slider.objects.filter(status=True)
        mobile_phones = Product.objects.filter(category__slug='mobile-phone').order_by('created')[:5]
        context['mobiles'] = []
        for product in mobile_phones:
            context['mobiles'].append(
                ShopProduct.objects.filter(product=product).first())

        context['festival'] = Advertisement.objects.filter(status=True, priority='festival').first()
        context['highPriorityAdv'] = Advertisement.objects.filter(status=True, priority='high-adv')[:2]
        context['foursomeAdv'] = Advertisement.objects.filter(status=True, priority='foursome-adv')
        context['twosomeAdv'] = Advertisement.objects.filter(status=True, priority='twosome-adv')
        laptops = Product.objects.filter(category__slug="laptop").order_by('created')[:5]
        context['laptops'] = []
        for product in laptops:
            context['laptops'].append(ShopProduct.objects.filter(product=product).first())
        # print(context['laptops'])
        context['logos'] = Logo.objects.get(title='logo')
        return context


class FooterView(TemplateView):
    template_name = 'base/footer.html'
    model = Logo
    template_name = "logos"
    
