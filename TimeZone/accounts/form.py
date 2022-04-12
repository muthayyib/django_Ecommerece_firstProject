
from django import forms
from . models import Account

class RegisterForm(forms.ModelForm):
    confirm_password =forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm password',
        'class':'form-control'
    }))
    class Meta:
        model = Account
        fields=['first_name','last_name','email','phone_number','password']
    
    def __init__(self,*args, **kwargs):
        super(RegisterForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='First name'
        self.fields['last_name'].widget.attrs['placeholder']='Last name'
        self.fields['email'].widget.attrs['placeholder']='Enter email'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter phone number'
        self.fields['password'].widget.attrs['placeholder']='Enter password'
        for field in self.fields:
            
            self.fields[field].widget.attrs['class']='form-control'
            self.fields[field].label = ''
    def clean(self):
        cleaned_data = super(RegisterForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password!= confirm_password:
            raise forms.ValidationError(
                'password does not match'
            )
        
        
                  
           

     
        

    