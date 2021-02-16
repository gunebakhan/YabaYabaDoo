from typing import overload
from django import forms
from django.forms.fields import TypedChoiceField

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]


class CartAddProductForm(forms.Form):
    quantity = TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput)
