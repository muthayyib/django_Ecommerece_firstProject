from cgi import print_exception
from curses.ascii import HT
from datetime import datetime
import json
from pickletools import read_int4
from urllib.robotparser import RequestRate
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from store.models import Product
from .forms import OrderForm
from cart.models import CartItem, Coupon
from orders.models import Order
from . models import OrderProduct, Payment, RazorPay
import datetime
import razorpay

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from cart.views import offer_check_function
from cart.models import CouponUsedUser


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

            cart_item = CartItem.objects.filter(user=current_user)
            
           
            order_data = Order.objects.get(order_number=order_number)
            # order_item = OrderProduct.objects.filter(order=order_data)
            
            sub_total=0
            for item in cart_item:
                new_price =  offer_check_function(item)
                sub_total += (new_price * item.quantity)
               
            if request.session:
                coupon_id = request.session.get('coupon_id')
                print(coupon_id)
            try:
                coupon = Coupon.objects.get(id=coupon_id)
                deduction = coupon.discount_amount(sub_total)
                sub_total = sub_total-deduction
                
            except:
                pass
        
            else:
                sub_total = sub_total

# authorize razorpay client with API Keys.
           
            #createe cliten
            razorpay_client = razorpay.Client(
            auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

            currency = 'INR'
            amount = sub_total*100

            #create order
            razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                            currency=currency,
                                                            payment_capture='1'))
            # order id of newly created order.
        
            razorpay_order_id = razorpay_order['id']
            callback_url = 'http://127.0.0.1:9000/orders/razor_success/'   
        
            # we need to pass these details to frontend.
            context = {
            'razorpay_order_id' : razorpay_order_id,
            'razorpay_merchant_key' : settings.RAZOR_KEY_ID,
            'razorpay_amount' : amount,
            'currency' : currency ,
            'callback_url' : callback_url,
            
            'order_data':order_data,
            'sub_total':sub_total,
            'cart_item':cart_item,

            }
            razor_model =RazorPay()
            razor_model.order = order_data
            razor_model.razor_pay = razorpay_order_id
            razor_model.save()
            return render(request,'orders/confirmation.html',context)
            
        else:
            return HttpResponse('form not valid')
        
    else:
        return redirect('checkout')

@csrf_exempt
def razor_success(request):
       
    transID = request.POST.get('razorpay_payment_id')
    razorpay_order_id = request.POST.get('razorpay_order_id')
    signature = request.POST.get('razorpay_signature')
    current_user = request.user
            #transaction details store
    razor = RazorPay.objects.get(razor_pay=razorpay_order_id)
    order = Order.objects.get(order_number = razor)

    payment = Payment()
    
    payment.payment_id = transID
    payment.payment_method = "Razorpapy"
    payment.amount_paid = order.order_total
    payment.status = "Completed"
    payment.save()
            
            
    
        
        
        
        
    context = {
                        
        'transID':transID,
        'order':order
                   

        }

            
        
    return render(request, 'payment/success.html',context)
    

    


   


def cash_on_delivery(request):
    return render(request,'payment/cod.html')

# ajax call 
def paypal_complete(request):
    body = json.loads(request.body)
    print('BODY:',body)
    current_user = request.user
    #transaction details store
    payment = Payment()
    payment.user= current_user
    payment.payment_id = body['transID']
    payment.payment_method = body['payment_method']
    payment.amount_paid = body['total']
    payment.status = body['status']
    payment.save()

    #create payment details and order product table
    
    cart_item = CartItem.objects.filter(user=current_user)
    order_id = str(body['orderID'])
    print(order_id)
    #taking order_id to show the invoice
    request.session['order_id']=order_id
    order_data = Order.objects.get(order_number = order_id)
    print(order_data,'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffopop')
    for item in cart_item:
        print('fffffffffffffffffffffffffffffffffffffffffffffffffffpay')
        OrderProduct.objects.create(
        order = order_data,
        product = item.product,
        user = current_user,
        quantity = item.quantity,
        product_price = item.product.price,
        payment = payment,
        ordered = True,
        )


        #decrease the product quantity from product
        orderproduct = Product.objects.filter(id=item.product_id).first()
        orderproduct.stock = orderproduct.stock-item.quantity
        orderproduct.save()
        #delete cart item from usercart after ordered
        CartItem.objects.filter(user=current_user).delete()
        
    if request.session.get('coupon_id'):
        coupon_id = request.session.get('coupon_id')
        del request.session['coupon_id']
        coupon = Coupon.objects.get(id=coupon_id)
        coupon_used = CouponUsedUser.objects.create(
        coupon = coupon,
        user=request.user,
                    )
        coupon_used.save()
    else:
        None
    return JsonResponse({'completed':'success'})

def paypal_complete_display(request):
    if request.session.get('order_id'):
        order_id = request.session.get('order_id')
        del request.session['order_id']
    else:
        return redirect('home')
    order = Order.objects.get(order_number = order_id )
    order_product = OrderProduct.objects.filter(order=order)
    transID = OrderProduct.objects.filter(order=order).first()
    context = {
        'order':order,
        'order_product':order_product,
        'transID':transID
    }
    return render(request,'payment/success.html',context)














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

def return_order(request,order_number):
    ord = Order.objects.get(order_number=order_number)
    ord.status='Returned'
    ord.save()
    return render (request,'orders/return_order.html',{'ord':ord})