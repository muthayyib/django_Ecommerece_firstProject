from django import forms

class CouponApplyForm(forms.Form):
    code = forms.CharField()
    code =forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter Coupon code',
        'class':'form-control',
    }))
    def __init__(self,*args, **kwargs):
        super(CouponApplyForm,self).__init__(*args, **kwargs)
        self.fields['code'].label = ''
