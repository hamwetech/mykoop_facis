from django import forms

from conf.utils import bootstrapify
from product.models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name']


class ProductUnitForm(forms.ModelForm):
    class Meta:
        model = ProductUnit
        fields = ['name', 'code']
        
        
class ProductVariationForm(forms.ModelForm):
    class Meta:
        model = ProductVariation
        fields = ['name', 'unit']


class ProductVariationPriceForm(forms.ModelForm):
    class Meta:
        model = ProductVariationPrice
        fields = ['product', 'unit', 'price']

       

bootstrapify(ProductForm)
bootstrapify(ProductUnitForm)
bootstrapify(ProductVariationForm)
bootstrapify(ProductVariationPriceForm)
