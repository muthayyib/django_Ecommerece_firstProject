from django import forms
from .models import Category

#form for product management
class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'
        