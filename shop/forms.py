from typing import overload
from django import forms
from django.db.models import fields
from django.forms.fields import TypedChoiceField
from .models import Shop, ShopOrder, ShopProduct


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]


class CartAddProductForm(forms.Form):
    quantity = TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput)


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = ShopOrder
        fields = ['discription']


class ShopProductForm(forms.ModelForm):
    class Meta:
        model = ShopProduct
        fields = ['color', 'price', 'quantity']


class CreateShopProductForm(forms.ModelForm):
    class Meta:
        model = ShopProduct
        fields = ['color', 'product', 'price', 'quantity']