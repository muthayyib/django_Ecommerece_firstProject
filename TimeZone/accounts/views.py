
from django.contrib import messages
from this import d
from django.shortcuts import redirect, render
import requests
from .models import Account
from . form import RegisterForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import random
from twilio.rest import Client
from cart.models import Cart,CartItem
from cart.views import _cart_id


# Create your views here.
def register(request):
    if request.user.is_authenticated:
        messages.info(request,'you are already logged in')
        return redirect('home')
    else:
        if request.method=='POST':
            form=RegisterForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone_number = form.cleaned_data['phone_number']
                password = form.cleaned_data['password']
                user_name=email.split("@")[0]
                user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,user_name=user_name,password=password)
                user.phone_number=phone_number
                user.save()
                messages.success(request,'You are successfully registered')
                return redirect('/')
        else:

            form = RegisterForm()
        context = {
            'form':form
        }
       
        return render (request, 'register.html',context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,email=email,password=password)
        if user is not None:
            try:
                print('try')
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exist = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exist :
                    cart_item = CartItem.objects.filter(cart=cart)
                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
            auth.login(request,user)
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                messages.success(request,'You are logged in succussfully')
                return redirect('/')
            # return render(request,'index.html')
        else:
            messages.error(request,'Invalid credentials')
            return redirect(login)
    return render (request, 'login.html')

def login_otp(request):
    if request.method=='POST':
        mobile='9562024224'
        phone_number = request.POST['phone_number']
        if mobile==phone_number:
            # Your Account SID from twilio.com/console
            account_sid = "ACae24b7b72fda67806f713a84ae269d11"
            # Your Auth Token from twilio.com/console
            auth_token  = "98c9ec770e77b68047cdcb010eb73c45"

            client = Client(account_sid, auth_token)
            global otp
            otp = str(random.randint(1000,9999))
            message = client.messages.create(
                to="+919562024224", 
                from_="+13349662693",
                body="Hello Thayyib! Your Login OTP is"+otp)
            messages.success(request,'OTP has been sent to 9562024224 & enter OTP')
            return render (request, 'login_otp1.html')

        else:
            messages.info(request,'invalid mobile number')
            return render (request, 'login_otp.html')
    return render (request, 'login_otp.html')

def login_otp1(request):
    if request.method=='POST':
        user = Account.objects.get(phone_number='9562024224')
        otpvalue = request.POST['otp']
        if otpvalue == otp:
            auth.login(request,user)
            messages.success(request,'You are logged in')
            return redirect('/')
            
        messages.error(request,'Invalid otp')
        return redirect(login_otp1)
    return render(request, 'login_otp1.html')

def my_profile(request):
    profile = Account.objects.get(first_name=request.user.first_name)
    print(profile)
    context = {
        'profile':profile
    }
    return render (request,'my_profile.html',context)

#profile edit
def my_profile_edit(request):
    profile = Account.objects.get(first_name=request.user.first_name)
    form = RegisterForm(instance=profile)
    if request.method =="POST":
        form = RegisterForm(request.POST,instance=profile)
        form.save()
        return redirect ('my_profile')
    return render (request,'my_profile_edit.html',{'form':form,'profile':profile})
   

    
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect(login)
