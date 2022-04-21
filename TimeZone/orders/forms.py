from dataclasses import fields
from django import forms
from . models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields= ['first_name','last_name','phone_number','email','address_line1','address_line2','country','state','city','zip','order_note']