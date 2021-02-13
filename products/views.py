from django.db.models.query_utils import PathInfo
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from braces.views import JSONResponseMixin, AjaxResponseMixin
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import ModelFormMixin, FormMixin
from django.utils import timezone
from .models import Product, Comment, ProductMeta, CommentLike, ImageGallery, Brand, Category, MobileMeta
from shop.models import ShopProduct, Shop
from .forms import CommentForm
from django.views import View
import json
from django.contrib import messages
from django.db.models import Count
from django.db.models import Min
from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.core import serializers
from django.db.models import Q


# Create your views here.


class AjaxableResponseMixin:
    def render_to_json_response(self, context, **response_kwargs):
        """Render a json response of context."""
        data = json.dumps(context)
        # data = serializers.serialize('json', context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).from_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        return response

    def form_valid(self, form):
        form = form.save(commit=False)
        form.author = self.request.user
        form.product = Product.objects.get(slug=self.kwargs.get('slug'))
        form.save()
        if self.request.is_ajax():
            # Request is ajax, send a json response
            data = {
                'title': form.title,
                'body': form.body,
            }
            return self.render_to_json_response(data)
        return super().form_valid(form)


class LaptopAjaxView(JSONResponseMixin, DetailView):
    model = Product
    content_type = 'application/javascript'
    json_dumps_kwargs = {'indent': 2}
    # template_name = 'products/single-product1.html'

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     context_dict = {
    #         'name': self.object.name,
    #         ''
    #     }


class LaptopDetail(AjaxableResponseMixin, FormMixin, DetailView):
    model = Product
    # template_name = 'products/single-product1.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('products:laptop_view', kwargs={'cat': self.kwargs.get('cat'), 'slug': self.kwargs.get('slug')})
    
    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response() is overridden.
        """
        if self.kwargs['cat'] == 'laptop':
            self.template_name = 'products/laptop-detail.html'
        elif self.kwargs['cat'] == 'mobile-phone':
            self.template_name = 'products/mobile-detail.html'

        if self.template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'")
        else:
            return [self.template_name]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        allcomments = Comment.objects.filter(draft=False, product=self.object)
        context['comments'] = allcomments
        print('s', allcomments)
        try:
            if self.kwargs['cat'] == 'laptop':
                meta = ProductMeta.objects.get(product=self.object)
            elif self.kwargs['cat'] == 'mobile-phone':
                meta = MobileMeta.objects.get(product=self.object)
        except:
            context['meta'] = None
        context['meta'] = meta

        likes = {}
        dislikes = {}
        author_likes = {}
        author_dislikes = {}

        rating = 0
        for comment in allcomments:
            rating += comment.rate
            likes[comment.id] = CommentLike.objects.filter(
                comment=comment, condition=True).count()
            dislikes[comment.id] = CommentLike.objects.filter(
                comment=comment, condition=False).count()
        try:
            context['rating'] = rating / allcomments.count()
        except Exception:
            context['rating'] = 0

        if self.request.user.is_authenticated:
            for comment in allcomments:
                author_likes[comment.id] = CommentLike.objects.filter(
                    comment=comment, condition=True, author=self.request.user)
                author_dislikes[comment.id] = CommentLike.objects.filter(
                    comment=comment, condition=False, author=self.request.user)

        context['likes'] = likes
        context['dislikes'] = dislikes
        context['author_likes'] = author_likes
        context['author_dislikes'] = author_dislikes

        shop_products = ShopProduct.objects.filter(product=self.object)
        shop_products = shop_products.filter(
            shop__closed=False, shop__status=True)
        shop_products = shop_products.exclude(quantity=0)
        shop_products = shop_products.order_by('price')
        context['shop_products'] = shop_products
        # print(shop_products.count())
        distinct = shop_products.order_by(
            'color').values_list('color').distinct()
        # shop_card = shop_products.filter(color__in=[item[0] for item in distinct])
        # print(shop_card.count())
        # distinct = shop_products.distinct('color').all()

        context['colors'] = []
        context['card_prodcts'] = {}
        for item in distinct:
            context['colors'].append(item[0])
            context['card_prodcts'][item[0]] = shop_products.order_by(
                'price').filter(color=item[0]).first()

        print(context['colors'])
        context['images'] = ImageGallery.objects.filter(product=self.object)

        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            print('ajax')
        else:
            return super().get(request, *args, **kwargs)

# Mobile Single View
class MobileView(DetailView):
    template_name = 'products/single-product1.html'
    model = Product
    context_object_name = 'single_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ProductsList(JSONResponseMixin, AjaxResponseMixin, ListView):
    model = Product
    template_name = 'products/laptop-list.html'
    ordering = ['-created', 'brand']
    paginate_by = 50

    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response() is overridden.
        """
        if self.kwargs['cat'] == 'laptop':
            self.template_name = 'products/laptop-list.html'
        elif self.kwargs['cat'] == 'mobile-phone':
            self.template_name = 'products/mobile-list.html'

        if self.template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'")
        else:
            return [self.template_name]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.kwargs.get('brand') is not None:
            return qs.filter(category__slug=self.kwargs['cat'], brand__slug=self.kwargs['brand'])

        return qs.filter(category__slug=self.kwargs['cat'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rating_dictionary = {}
        prices = {}
        shops = {}
        for product in self.object_list:
            price = ShopProduct.objects.filter(product=product).values_list(
                'shop').annotate(Min('price')).order_by('price')

            prices[product.id] = price[0][1]
            shops[product.id] = get_object_or_404(Shop, id=price[0][0])

            comments = product.comment.filter(draft=False)
            ratings = 0
            for comment in comments:
                ratings += comment.rate
            try:
                rating_dictionary[product.id] = (
                    comments.count(), ratings/comments.count())
            except Exception:
                rating_dictionary[product.id] = (
                    comments.count(), 0)
                # print('zero')

        context['rating'] = rating_dictionary
        context['prices'] = prices
        context['shops'] = shops
        context['cat'] = self.kwargs['cat']

        if self.kwargs['cat'] == 'laptop':
            context = self.get_laptop_context(context)
        elif self.kwargs['cat'] == 'mobile-phone':
            context = self.get_mobile_context(context)

        return context

    def get_laptop_context(self, context):
        categroy = Category.objects.get(slug=self.kwargs['cat'])
        meta = ProductMeta.objects.all()
        context['display_touchable'] = meta.order_by(
            'display_touchable').values_list('display_touchable').distinct()
        context['rams'] = meta.order_by(
            'ram_capacity').values_list('ram_capacity').distinct()
        context['cpu_series'] = meta.order_by(
            'cpu_series').values_list('cpu_series').distinct()
        context['storages'] = meta.order_by(
            'storage').values_list('storage').distinct()
        context['brands'] = Brand.objects.filter(product_type=categroy)
        context['display_accuracies'] = meta.order_by(
            'display_accuracy').values_list('display_accuracy').distinct()
        context['ram_types'] = meta.order_by(
            'ram_type').values_list('ram_type').distinct()
        context['gpu_manufacturers'] = meta.order_by(
            'gpu_manufacturer').values_list('gpu_manufacturer').distinct()
        context['display_mates'] = meta.order_by(
            'display_mate').values_list('display_mate').distinct()

        return context

    def get_mobile_context(self, context):
        categroy = Category.objects.get(slug=self.kwargs['cat'])
        context['brands'] = Brand.objects.filter(product_type=categroy)
        meta = MobileMeta.objects.all()
        context['back_camera_modules'] = meta.order_by(
            'back_camera_modules').values_list('back_camera_modules').distinct()
        context['num_sim_cards'] = meta.order_by(
            'num_sim_cards').values_list('num_sim_cards').distinct()
        context['sim_card_desc'] = meta.order_by(
            'sim_card_desc').values_list('sim_card_desc').distinct()
        context['display_technos'] = meta.order_by(
            'display_techno').values_list('display_techno').distinct()
        context['image_resolutions'] = meta.order_by(
            'image_resolution').values_list('image_resolution').distinct()
        context['rams'] = meta.order_by(
            'ram').values_list('ram').distinct()
        context['ram_capacities'] = meta.order_by(
            'ram_capacity').values_list('ram_capacity').distinct()
        context['sizes'] = meta.order_by(
            'display_size').values_list('display_size').distinct()
        context['os_releases'] = meta.order_by(
            'os_release').values_list('os_release').distinct()
        context['OS'] = meta.order_by(
            'os').values_list('os').distinct()
        return context

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', 'created')

        if ordering == 'price':
            pass
        # validate ordering here
        return ordering

    def get_ajax(self, request, *args, **kwargs):
        if self.kwargs['cat'] == 'laptop':
            data = self.laptop_ajax(request, *args, **kwargs)
        if self.kwargs['cat'] == 'mobile-phone':
            data = self.mobile_ajax(request, *args, **kwargs)
        return self.render_json_response(data)

    def laptop_ajax(self, request, *args, **kwargs):
        data = request.GET.getlist('data[]', None)
        search_fields = {'brand': [], 'touch': [], 'mate': [], 'gpu': [], 'ramType': [
        ], 'resolution': [], 'storage': [], 'ramCapacity': [], 'cpu': []}

        for datum in data:
            if datum.startswith('brand'):
                search_fields['brand'].append(datum.split('_')[1])
            elif datum.startswith('touch'):
                search_fields['touch'].append(datum.split('_')[1] == 'True')
            elif datum.startswith('mate'):
                search_fields['mate'].append(datum.split('_')[1])
            elif datum.startswith('gpu'):
                search_fields['gpu'].append(datum.split('_')[1])
            elif datum.startswith('ramType'):
                search_fields['ramType'].append(datum.split('_')[1])
            elif datum.startswith('resolution'):
                search_fields['resolution'].append(datum.split('_')[1])
            elif datum.startswith('storage'):
                search_fields['storage'].append(datum.split('_')[1])
            elif datum.startswith('ramCapacity'):
                search_fields['ramCapacity'].append(datum.split('_')[1])
            elif datum.startswith('cpu'):
                search_fields['cpu'].append(datum.split('_')[1])
            elif datum.startswith('views'):
                search_fields['views'] = 'views'
            elif datum.startswith('sell'):
                search_fields['sell'] = 'sell'
            elif datum.startswith('popular'):
                search_fields['popular'] = 'rate'
            elif datum.startswith('new'):
                search_fields['new'] = 'created'
            elif datum.startswith('cheap'):
                search_fields['price'] = 'price'
            elif datum.startswith('expensive'):
                search_fields['price'] = '-price'

        print(search_fields)
        product_list = ProductMeta.objects.all()
        if search_fields.get('gpu', None):
            # print(search_fields.get('gpu', None))
            product_list = product_list.filter(
                gpu_manufacturer__in=search_fields['gpu'])
            # print(product_list.count())
        if search_fields.get('ramType', None):
            product_list = product_list.filter(
                ram_type__in=search_fields['ramType'])
            # print(product_list.count())

        if search_fields.get('resolution', None):
            product_list = product_list.filter(
                display_accuracy__in=search_fields['resolution'])
            # print(product_list.count())

        if search_fields.get('storage', None):
            product_list = product_list.filter(
                storage__in=search_fields['storage'])
            # print(product_list.count())

        if search_fields.get('ramCapacity', None):
            product_list = product_list.filter(
                ram_capacity__in=search_fields['ramCapacity'])
            print(product_list.count())

        if search_fields.get('cpu', None):
            product_list = product_list.filter(
                cpu_series__in=search_fields['cpu'])
            # print(product_list.count())

        if search_fields.get('touch', None):
            product_list = product_list.filter(
                display_touchable__in=search_fields['touch'])
        if search_fields.get('mate', None):
            product_list = product_list.filter(
                display_mate__in=search_fields['mate'])

        product_list = product_list.values_list('product', flat=True)
        product_list = Product.objects.filter(pk__in=product_list)

        if search_fields.get('new', None):
            product_list = product_list.order_by(search_fields['new'])
        if search_fields.get('brand', None):
            brands = Brand.objects.filter(name__in=search_fields['brand'])
            product_list = product_list.filter(brand__in=brands)

        rating_dictionary = {}
        prices = {}
        shops = {}
        product_ids = []
        for product in product_list:
            product_ids.append(f"{product.id}")
            price = ShopProduct.objects.filter(product=product).values_list(
                'shop').annotate(Min('price')).order_by('price')

            prices[f"{product.id}"] = str(price[0][1])
            shops[f"{product.id}"] = Shop.objects.filter(
                id=price[0][0]).first().name
            comments = product.comment.filter(draft=False)
            ratings = 0
            for comment in comments:
                ratings += comment.rate
            try:
                rating_dictionary[f"{product.id}"] = (
                    comments.count(), ratings/comments.count())
            except Exception:
                rating_dictionary[f"{product.id}"] = (
                    comments.count(), 0)

        # sort based on price 
        if search_fields.get('price', None):
            product_ids = []
            sorted_p = {k: v for k, v in sorted(
                prices.items(), key=lambda item: item[1])}
            for key in sorted_p:
                product_ids.append(key)
            if search_fields['price'] == '-price':
                product_ids.reverse()
        
        if search_fields.get('popular', None):
            product_ids = sorted(
                rating_dictionary, key=lambda k: rating_dictionary[k][0])
            product_ids.reverse()

        # print({k: v for k, v in sorted(
        #     rating_dictionary.items(), key=lambda item: item[1])})
        product_name_image = {}
        for product in product_list:
            product_name_image[f"{product.id}"] = (
                product.name, product.image.url, product.slug)

        product_list = serializers.serialize('json', product_list)
        data = {
            'product_list': product_name_image,
            'rating_dictionary': rating_dictionary,
            'prices': prices,
            'shops': shops,
            'cat': self.kwargs['cat'],
            'product_ids': product_ids,
        }
        return data

    def mobile_ajax(self, request, *args, **kwargs):
        data = request.GET.getlist('data[]', None)
        search_fields = {'brand': [], 'camModule': [], 'net': [], 'numSimCard': [],
                         'simDesc': [], 'displayTechno': [], 'imageResolution': [],
                         'storage': [], 'ramCapacity': [], 'size': [], 'osRelease': [],
                         'os': [],
                         }

        for datum in data:
            if datum.startswith('brand'):
                search_fields['brand'].append(datum.split('_')[1])
            elif datum.startswith('camModule'):
                search_fields['camModule'].append(
                    datum.split('_')[1])
            elif datum.startswith('net'):
                search_fields['net'].append(datum.split('_')[1])
            elif datum.startswith('numSimCard'):
                search_fields['numSimCard'].append(datum.split('_')[1])
            elif datum.startswith('simDesc'):
                search_fields['simDesc'].append(datum.split('_')[1])
            elif datum.startswith('displayTechno'):
                search_fields['displayTechno'].append(datum.split('_')[1])
            elif datum.startswith('imageResolution'):
                search_fields['imageResolution'].append(datum.split('_')[1])
            elif datum.startswith('storage'):
                search_fields['storage'].append(datum.split('_')[1])
            elif datum.startswith('ramCapacity'):
                search_fields['ramCapacity'].append(datum.split('_')[1])
            elif datum.startswith('size'):
                search_fields['size'].append(datum.split('_')[1])
            elif datum.startswith('osRelease'):
                search_fields['osRelease'].append(datum.split('_')[1])
            elif datum.startswith('os'):
                search_fields['os'].append(datum.split('_')[1])
            elif datum.startswith('views'):
                search_fields['views'] = 'views'
            elif datum.startswith('sell'):
                search_fields['sell'] = 'sell'
            elif datum.startswith('popular'):
                search_fields['popular'] = 'rate'
            elif datum.startswith('new'):
                search_fields['new'] = 'created'
            elif datum.startswith('cheap'):
                search_fields['price'] = 'price'
            elif datum.startswith('expensive'):
                search_fields['price'] = '-price'
        
        # print(search_fields)
        product_list = MobileMeta.objects.all()
        if search_fields.get('camModule', None):
            # print(search_fields.get('gpu', None))
            product_list = product_list.filter(
                back_camera_modules__in=search_fields['camModule'])
            # print(product_list.count())
        if search_fields.get('net', None):
            product_list = product_list.filter(
                networks__in=search_fields['net'])
            # print(product_list.count())

        if search_fields.get('numSimCard', None):
            product_list = product_list.filter(
                num_sim_cards__in=search_fields['numSimCard'])
            # print(product_list.count())

        if search_fields.get('simDesc', None):
            product_list = product_list.filter(
                sim_card_desc__in=search_fields['simDesc'])
            # print(product_list.count())

        if search_fields.get('displayTechno', None):
            product_list = product_list.filter(
                display_techno__in=search_fields['displayTechno'])
            # print(product_list.count())

        if search_fields.get('imageResolution', None):
            product_list = product_list.filter(
                image_resolution__in=search_fields['imageResolution'])
            # print(product_list.count())

        if search_fields.get('storage', None):
            product_list = product_list.filter(
                ram__in=search_fields['storage'])

        if search_fields.get('ramCapacity', None):
            product_list = product_list.filter(
                ram_capacity__in=search_fields['ramCapacity'])

        if search_fields.get('size', None):
            product_list = product_list.filter(
                size__in=search_fields['size'])

        if search_fields.get('osRelease', None):
            product_list = product_list.filter(
                os_release_in=search_fields['osRelease'])
        
        if search_fields.get('os', None):
            product_list = product_list.filter(
                os__in=search_fields['os'])

        product_list = product_list.values_list('product', flat=True)
        product_list = Product.objects.filter(pk__in=product_list)

        if search_fields.get('new', None):
            product_list = product_list.order_by(search_fields['new'])

        if search_fields.get('brand', None):
            brands = Brand.objects.filter(name__in=search_fields['brand'])
            product_list = product_list.filter(brand__in=brands)

        rating_dictionary = {}
        prices = {}
        shops = {}
        product_ids = []
        for product in product_list:
            product_ids.append(f"{product.id}")
            price = ShopProduct.objects.filter(product=product).values_list(
                'shop').annotate(Min('price')).order_by('price')

            prices[f"{product.id}"] = str(price[0][1])
            shops[f"{product.id}"] = Shop.objects.filter(
                id=price[0][0]).first().name
            comments = product.comment.filter(draft=False)
            ratings = 0
            for comment in comments:
                ratings += comment.rate
            try:
                rating_dictionary[f"{product.id}"] = (
                    comments.count(), ratings/comments.count())
            except Exception:
                rating_dictionary[f"{product.id}"] = (
                    comments.count(), 0)
        
         # sort based on price
        if search_fields.get('price', None):
            product_ids = []
            sorted_p = {k: v for k, v in sorted(
                prices.items(), key=lambda item: item[1])}
            for key in sorted_p:
                product_ids.append(key)
            if search_fields['price'] == '-price':
                product_ids.reverse()

        if search_fields.get('popular', None):
            product_ids = sorted(
                rating_dictionary, key=lambda k: rating_dictionary[k][0])
            product_ids.reverse()

        product_name_image = {}
        for product in product_list:
            product_name_image[f"{product.id}"] = (
                product.name, product.image.url, product.slug)

        product_list = serializers.serialize('json', product_list)
        data = {
            'product_list': product_name_image,
            'rating_dictionary': rating_dictionary,
            'prices': prices,
            'shops': shops,
            'cat': self.kwargs['cat'],
            'product_ids': product_ids,
        }
        return data

    # def get(self, request, *args, **kwargs):
    #     self.object_list = self.get_queryset()
    #     context = self.get_context_data()
    #     if self.request.is_ajax():
    #         ram = request.GET.getlist('ram[]', None)

    #         # product_list = ProductMeta.objects.filter(
    #         #     ram_capacity=ram[0]).product.all()
    #         product_list = ProductMeta.objects.filter(ram_capacity=ram[0]).values_list('product', flat=True)
    #         product_list = Product.objects.filter(pk__in=product_list)

    #         context['product_list'] = product_list
    #         for p in context['product_list']:
    #             print(p.slug)

    #         return super().get(request, *args, **kwargs)
    #         # return self.render_to_response(context)
    #         # return HttpResponse('hi')
    #     else:
        # print('hi')
        # return super().get(request, *args, **kwargs)


def like_comment(request):
    user = request.user
    if request.POST.get('action') == 'post':
        comment_id = str(request.POST.get('id'))
        comment_id = json.loads(comment_id)
        like_type = str(request.POST.get('like_type'))
        if like_type == 'like':
            status = True
        else:
            status = False
        comment = Comment.objects.get(id=comment_id)
        comment_like = CommentLike(
            author=user, comment=comment, condition=status)
        comment_like.save()
        like_counts = CommentLike.objects.filter(
            comment=comment, condition=status).count()
        response = {'like_counts': like_counts}
        response = json.dumps(response)
        return HttpResponse(response, status=201)

    return HttpResponse(json.dumps({'comment_id': -1}))
