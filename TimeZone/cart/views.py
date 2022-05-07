from pickle import OBJ
from re import sub
from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product
from . models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from datetime import datetime
from . models import Coupon
from django.utils import timezone
import pytz
from adminpanel.models import ProductOffer
from adminpanel.models import CategoryOffer

from .forms import CouponApplyForm
# Create your views here.
def offer_check_function(item):
    product = Product.objects.get(product_name=item)
    print(product)
    if ProductOffer.objects.filter(product=product).exists():
        if product.pro_offer:
            sub_total = product.price - product.price*product.pro_offer.discount/100
    elif CategoryOffer.objects.filter(category=item.product.category).exists():
           if item.product.category.cat_offer:
               sub_total = product.price - product.price*item.product.category.cat_offer.discount/100
    else:
        sub_total=product.price
        print(sub_total)
    return sub_total
        
    

    
    


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
    if request.user.is_authenticated:
        try:
            
            cart_item =  CartItem.objects.get(product=product,cart=cart,user=request.user)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity = 1,
                cart = cart,
                user = request.user,
            )

            cart_item.save()
    else:
        try:
            
            cart_item =  CartItem.objects.get(product=product,cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity = 1,
                cart = cart,
            )

            cart_item.save()
    
    return redirect('store')

def remove_cart(request,product_id):
    
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product,user=request.user)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

#delete an item from cart
def delete_item(request,product_id):
    
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(product=product,user=request.user).first()
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, sub_total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
            cart_count = CartItem.objects.filter(user=request.user,is_active=True).count()
            
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            cart_count = CartItem.objects.filter(cart=cart, is_active=True).count()
        
       
    except:
        pass #just ignore

    context = {
        'sub_total': sub_total,
        'quantity': quantity,
        'cart_items': cart_items,
        'cart_count':cart_count
    }
    return render(request, 'store/cart.html', context)    

@login_required
def checkout(request, sub_total=0, quantity=0, cart_items=None,coupon=None, final_price=0,deduction =0):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            new_price =  offer_check_function(cart_item)
            sub_total += (new_price * cart_item.quantity)
            print('heheeh')
    except:
        pass #just ignore
    coupon_apply_form = CouponApplyForm()
   
    if request.session:
        coupon_id = request.session.get('coupon_id')
        print(coupon_id)
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            deduction = coupon.discount_amount(sub_total)
            final_price = sub_total-deduction
            print(final_price)
        except:
            pass
        
    else:
        sub_total = sub_total

        
    context = {
        'sub_total': sub_total,
        'final_price':final_price,
        'quantity': quantity,
        'cart_items': cart_items,
        'coupon_apply_form':coupon_apply_form,
        'coupon':coupon,
        'deduction':deduction,

    }
    return render (request,'cart/checkout.html',context)
    
def coupon_apply(request):
    now = timezone.now()
    
    form = CouponApplyForm(request.POST)
    print(now)
    if form.is_valid():
        
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,valid_from__lte=now,valid_to__gte=now,active=True)
            request.session['coupon_id']=coupon.id
            return redirect('checkout')
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            return redirect('checkout')

