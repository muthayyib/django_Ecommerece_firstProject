from cgi import print_exception
from curses.ascii import HT
from datetime import datetime
import json
from pickletools import read_int4
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from store.models import Product
from .forms import OrderForm
from cart.models import CartItem, Coupon
from orders.models import Order
from . models import OrderProduct
import datetime
import razorpay

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from cart.views import offer_check_function


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


            #     #decrease the product quantity from product
            #     orderproduct = Product.objects.filter(id=item.product_id).first()
            #     orderproduct.stock = orderproduct.stock-item.quantity
            #     orderproduct.save()
            # #delete cart item from usercart after ordered
            # CartItem.objects.filter(user=current_user).delete()

           
            order_data = Order.objects.get(order_number=order_number)
            order_item = OrderProduct.objects.filter(order=order_data)
            
            sub_total=0
            for item in order_item:
                new_price =  offer_check_function(item)
                sub_total += (new_price * item.quantity)
                print(sub_total)
                print(item,'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
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
            context = {
                    'order_data':order_data,
                    'order_item':order_item,
                    'sub_total':sub_total,
                    'ordereditem':ordereditem,
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

def return_order(request,order_number):
    ord = Order.objects.get(order_number=order_number)
    ord.status='Returned'
    ord.save()
    return render (request,'orders/return_order.html',{'ord':ord})


# authorize razorpay client with API Keys.

    
def payments(request):
    currency = 'INR'

    amount = '200000'
    razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
   
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    return render(request,'orders/payments.html',context=context)

# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    print('HAI IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
    # only accept POST request.
    if request.method == "POST":
        print('HAI IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            print(payment_id,'*'*100)
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            razorpay_client = razorpay.Client(
            auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    # return render(request, 'paymentsuccess.html')
                    return HttpResponse('thayyib kazinj')
                except:
 
                    # if there is an error while capturing payment.
                    return HttpResponse('ivide und taaaaaaaaaaaa error')
            else:
 
                # if signature verification fails.
                # return render(request, 'paymentfail.html')
                return render(request,'payment/razor_success.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

def cash_on_delivery(request):
    return render(request,'payment/cod.html')

# def paymentComplete(request):
#     body = json.loads(request.body)
#     print('BODY:',body)
#     return JsonResponse('payment completed',safe =False)