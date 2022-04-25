from django import forms
from orders.models import Order



class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields= '__all__'