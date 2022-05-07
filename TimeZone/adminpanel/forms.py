from django import forms
from orders.models import Order
from . models import CategoryOffer, ProductOffer
from cart.models import Coupon



class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields= '__all__'

#to get a calendar for add and edit the offers
class DateTimeLocal(forms.DateTimeInput):
    input_type = 'datetime-local'
    color ='Red'



class CategoryOfferForm(forms.ModelForm):
    class Meta:
        model = CategoryOffer
        fields = '__all__'
        widgets = {
            'valid_from': DateTimeLocal(),
            'valid_to': DateTimeLocal(),
        }

class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffer
        fields = '__all__'
        widgets = {
            'valid_from': DateTimeLocal(),
            'valid_to': DateTimeLocal(),
        }


class CouponAdminForm(forms.ModelForm):   
    class Meta:
        model = Coupon
        fields = '__all__'
        widgets = {
            'valid_from': DateTimeLocal(),
            'valid_to': DateTimeLocal(),
        }

# class OrderFilter()
