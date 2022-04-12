

from django.urls import path
from . import views
from django import forms

class formf(forms.ModelForm):
    pass


urlpatterns = [
    
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('loginotp/',views.login_otp,name='login_otp'),
    path('login_otp1',views.login_otp1,name='login_otp1'),
    path('logout/',views.logout, name='logout'),
]
