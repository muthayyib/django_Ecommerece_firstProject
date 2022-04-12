from django import forms
from .models import Product

#form for product management
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        