from cgi import print_exception
from datetime import datetime
from pickletools import read_int4
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from store.models import Product
from .forms import OrderForm
from cart.models import CartItem
from orders.models import Order
from . models import OrderProduct
import datetime

# Create your views here.
def place_order(request,total = 0,quantity = 0):
    current_user = request.user

    #if cart is empty return to login
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if (cart_count <= 0):
        return redirect('store')
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity


    if request.method=='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            #store all billing info
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone_number = form.cleaned_data['phone_number']
            data.email = form.cleaned_data['email']
            data.address_line1 = form.cleaned_data['address_line1']
            data.address_line2 = form.cleaned_data['address_line2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.zip = form.cleaned_data['zip']
            data.order_note = form.cleaned_data['order_note']
            data.order_total=total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            #generate order number yr/m/day/hr/mn/second
            order_number = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            data.order_number = order_number
            data.save()

            ordereditem = CartItem.objects.filter(user=current_user)
            
            for item in ordereditem:
                OrderProduct.objects.create(
                    order = data,
                    product = item.product,
                    user = current_user,
                    quantity = item.quantity,
                    product_price = item.product.price,
                    ordered = True,

                )


                #decrease the product quantity from product
                orderproduct = Product.objects.filter(id=item.product_id).first()
                orderproduct.stock = orderproduct.stock-item.quantity
                orderproduct.save()
            #delete cart item from usercart after ordered
            CartItem.objects.filter(user=current_user).delete()

            messages.success(request,"your order has been placed successfully")
            order_data = Order.objects.get(order_number=order_number)
            order_item = OrderProduct.objects.filter(order=order_data)
            g_total=0
            for item in order_item:
                subr_total = item.product_price * item.quantity
                g_total = g_total + subr_total
            context = {
                    'order_data':order_data,
                    'order_item':order_item,
                    'g_total':g_total
            }
            return render(request,'orders/confirmation.html',context)
        else:
            return HttpResponse('jithin raj mm')
        
    else:
        return redirect('checkout')



def my_orders(request):
    current_user = request.user

    orders = Order.objects.filter(user=current_user)

    
    
    context ={
        'orders':orders,
        
    }
    return render(request,'orders/my_orders.html',context)

def order_view(request,id):
    ord = Order.objects.filter(order_number=id).filter(user=request.user).first()
    orders = OrderProduct.objects.filter(order=ord)
    
    context ={
        'orders':orders,
        'ord':ord
    }
    return render(request,'orders/order_view.html',context)

def order_cancel_user(request,order_number):
    ord = Order.objects.get(order_number=order_number)
    ord.status='Cancelled'
    ord.save()
    return redirect('my_orders')
