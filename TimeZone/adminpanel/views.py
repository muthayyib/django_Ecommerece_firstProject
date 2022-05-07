
from csv import writer
from datetime import datetime
from multiprocessing.sharedctypes import Value
import os
from socket import IPV6_DONTFRAG
from urllib import response
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from pkg_resources import get_default_cache
from cart.models import Coupon
from adminpanel.models import CategoryOffer, ProductOffer
from adminpanel.forms import OrderEditForm
from accounts.form import RegisterForm
from accounts.models import Account
from store.models import Product
from category.models import Category
from store.forms import ProductForm
from category.forms import CategoryForm
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from orders.models import Order,OrderProduct
from django.db.models.functions import ExtractMonth,ExtractDay
from django.db.models import Count
import calendar
import csv
import xlwt
from django.template.loader import render_to_string
from weasyprint import HTML, html
import tempfile

from . forms import CategoryOfferForm,ProductOfferForm,CouponAdminForm

# Create your views here.

#admin login
def login_admin(request):
    if request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,email=email,password=password)
        if user is not None:
            if user.is_admin==True:
                auth.login(request,user)
                return render(request, 'admin_panel/dashboard_adm.html')
        context={'message':'invalid credentials','class':'danger'}
        return render (request,'admin_panel/login_admin.html',context)
    else:
        return render (request,'admin_panel/login_admin.html')

#admin logout
def logout_admin(request):
    auth.logout(request)
    return redirect(login_admin)
@login_required(login_url='/newadmin/')

#admin dashboard

def dashboard(request):
    #ORDER GRAPH
    orderbyday = Order.objects.annotate(day=ExtractDay('created_at')).values('day').annotate(count=Count('id'))
    print(orderbyday)
    dayday =[]
    orderperday =[]
    for o in orderbyday:
        dayday.append(o['day'])
        orderperday.append(o['count'])
    order = Order.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id')).values('month','count')
    monthNumber = []
    totalOrder = []
    for ord in order:
        monthNumber.append(calendar.month_name[ord['month']])
        totalOrder.append(ord['count'])
    #total users
    users_count = Account.objects.all().count()

    #total revenue
    revenue=0
    order = OrderProduct.objects.all()
    for item in order:
        revenue = revenue + item.product_price

    #total order
    order_count = Order.objects.all().count()

    
    # order_status = Order.objects.annotate(status=Value(Ac)).values('statu').annotate(count=Count('id'))
    # status_status =[]
    # status_count =[]
    
    # print(order_status)
    completed_order = Order.objects.filter(status='Completed').count()
    pending_order = Order.objects.filter(status='New').count()
    accepted_order = Order.objects.filter(status='Accepted').count()
    order_status_list = []
    order_status_list.append(completed_order)
    order_status_list.append(accepted_order)
    order_status_list.append(pending_order)
    print(order_status_list)

    context = {
        'monthNumber':monthNumber,
        'totalOrder':totalOrder,
        'dayday':dayday,
        'orderperday':orderperday,
        'users_count':users_count,
        'revenue':revenue,
        'order_count':order_count,
        'order_status_list':order_status_list,
        # 'today_revenue':today_revenue,
        }
    
    return render (request,'admin_panel/dashboard_adm.html',context)

#csv export
def export_csv(request):
    response = HttpResponse(content_type='text/csf')
    response['Content-Disposition']='attachement; filename=Expenses' + str(datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Amount','name','date','order'])
    orders = Order.objects.filter(status='Completed')
    for i in orders:
        writer.writerow([i.first_name])
    return response

#excel export 
def export_excel(request):
    response = HttpResponse(content_type='applications/ms-excel')
    response['Content-Disposition']='attachement; filename=Expenses' + str(datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws =wb.add_sheet('Expenses')
    row_num=0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['first_name','last_name','order_number','status']
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    font_style = xlwt.XFStyle()
    
    rows = Order.objects.all().values_list('first_name','last_name','order_number','status')
    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)
    wb.save(response)
    return response

#export to pdf
def export_pdf(request):
    response = HttpResponse(content_type='applications/pdf')
    response['Content-Disposition']='attachement; inline; filename=Expenses' + str(datetime.now())+'.pdf'
    response['Content-Transfer-Encoding']='binary'
    orders = Order.objects.all()
    context ={
        'orders':orders,

    }
    html_string = render_to_string('admin_panel/pdf_output.html',context)
    html = HTML(string=html_string)
    result = html.write_pdf()


    with tempfile.NamedTemporaryFile(delete=True) as output: 
        output.write(result)
        output.flush()

        output = open(output.name,'rb')
        response.write(output.read())
    return response



#user view admin side
def users_adm(request):
    user_list = Account.objects.all()
    context={'user_list':user_list}
    return render(request,'admin_panel/users_adm.html',context)

#user details for admin

def user_detail(request,id):
    eachUser = Account.objects.get(id=id)
    context = {'eachUser':eachUser}
    return render(request,'user_detail.html',context)

#user activate
def activateUser(request,id):
    user = Account.objects.get(id=id)
    user.is_active = True
    user.save()
    return redirect(users_adm)



#user deactivation 
def deactivateUser(request,id):
    user = Account.objects.get(id=id)
    user.is_active = False
    user.save()
    return redirect(users_adm)

#product view admin side
def product_view(request):
    product_list = Product.objects.all()
    context= {'product_list':product_list}
    return render (request,'admin_panel/product_view.html',context)

#category view admin side
def category_view(request):
    category_list= Category.objects.all()
    context = {'category_list': category_list}
    return render (request,'admin_panel/category_view.html',context)

#add categoris by admin
def add_category(request):
    form = CategoryForm(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        messages.info(request,'Category added successfully')
        return redirect(category_view)
    context ={
        'form':form
    }
    return render (request,'admin_panel/add_category.html',context)

#edit category
def edit_category(request,id):
    category = Category.objects.get(id=id)
    form = CategoryForm(instance=category)
    if request.method =="POST":
        form = CategoryForm(request.POST,request.FILES,instance=category)
        if len(request.FILES)!=0:
            if len(category.cat_img)>0:
                os.remove(category.cat_img.path)
        form.save()
        messages.success(request,'Category updated successfully')
        return redirect('category_view')
    return render (request,'admin_panel/edit_category.html',{'form':form,'category':category})

#delete category by admin
def delete_category(request,id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect(category_view)

#add product by admin
def add_product(request):
    form = ProductForm(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        messages.info(request,'Product added successfully')
        return redirect('product_view')
    context = {'form':form}
    return render(request,'admin_panel/add_product.html',context)

#edit product by admin
def edit_product(request,id):
    product = Product.objects.get(id=id)
    form = ProductForm(instance=product)
    if request.method =="POST":
        form = ProductForm(request.POST,request.FILES,instance=product)
        if len(request.FILES)!=0:
            if len(product.images)>0:
                os.remove(product.images.path)
            product.images = request.FILES['images']
            product.save()
            messages.success(request,'Product edited successfully')
            return redirect('product_view')
    return render (request,'admin_panel/edit_product.html',{'form':form,'product':product})

#delete product by admin
def delete_product(request,id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect(product_view)

#order mangement
def order_manage(request):
    orders = OrderProduct.objects.all()
    context = {
        'orders':orders,
        
    }
    return render (request,'admin_panel/order_manage.html',context)

def order_cancel(request,order_number):
    orders = Order.objects.get(order_number=order_number)
    orders.status ='Cancelled'
    orders.save()
    return redirect ('order_manage')

def change_status(request,order_number):
    orders = Order.objects.get(order_number=order_number)
    form = OrderEditForm(instance=orders)
    if request.method=='POST':
        form = OrderEditForm(request.POST)
        status = request.POST.get('status')
        orders.status = status
        orders.save()
        return redirect ('order_manage')
    context = {
        'orders':orders,
        'form':form
    }
    return render(request,'admin_panel/edit_statu.html',context)

#offer management 
def offer_view(request):
    cat_offer = CategoryOffer.objects.all()
    pro_offer = ProductOffer.objects.all()
    coupon = Coupon.objects.all()
    context={
        'cat_offer':cat_offer,
        'pro_offer':pro_offer,
        'coupon':coupon,
    }
    return render (request,'admin_panel/offer_view.html',context)

#product offer edit
def edit_pro_offer(request,id):
    offer = ProductOffer.objects.get(id=id)
    form = ProductOfferForm(instance=offer)
    if request.method =="POST":
        form = ProductOfferForm(request.POST,instance=offer)
        form.save()
        messages.success(request,'Product offer updated successfully')
        return redirect('offer_view')
    return render (request,'admin_panel/edit_pro_offer.html',{'form':form,'offer':offer})

#category offer edit pro_
def edit_cat_offer(request,id):
    offer = CategoryOffer.objects.get(id=id)
    form = CategoryOfferForm(instance=offer)
    if request.method =="POST":
        form = CategoryOfferForm(request.POST,instance=offer)
        form.save()
        messages.success(request,'Category offer updated successfully')
        return redirect('offer_view')
    return render (request,'admin_panel/edit_cat_offer.html',{'form':form,'offer':offer})

#add category offer
def add_cat_offer(request):
    form = CategoryOfferForm(request.POST)
    if form.is_valid():
        form.save()
        messages.info(request,'Category added successfully')
        return redirect(offer_view)
    context ={
        'form':form
    }
    return render (request,'admin_panel/add_cat_offer.html',context)
#add product offer
def add_pro_offer(request):
    form = ProductOfferForm(request.POST)
    if form.is_valid():
        form.save()
        messages.info(request,'Product offer added successfully')
        return redirect(offer_view)
    context ={
        'form':form
    }
    return render (request,'admin_panel/add_pro_offer.html',context)

#delete category by admin
def delete_cat_offer(request,id):
    offer = CategoryOffer.objects.filter(id=id)
    offer.delete()
    return redirect(offer_view)

#delete category by admin
def delete_pro_offer(request,id):
    offer = ProductOffer.objects.get(id=id)
    offer.delete()
    return redirect(offer_view)

#coupon amaaasdfhasdffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff coupon
#add product offer
def add_coupon(request):
    form = CouponAdminForm(request.POST)
    if form.is_valid():
        form.save()
        messages.info(request,'coupon added successfully')
        return redirect(offer_view)
    context ={
        'form':form
    }
    return render (request,'admin_panel/add_coupon.html',context)
#edit coupons
def edit_coupon(request,id):
    coupon = Coupon.objects.get(id=id)
    form = CouponAdminForm(instance=coupon)
    if request.method =="POST":
        form = CouponAdminForm(request.POST,instance=coupon)
        form.save()
        messages.success(request,'coupon updated successfully')
        return redirect('offer_view')
    return render (request,'admin_panel/edit_coupon.html',{'form':form,'coupon':coupon})

#delete category by admin
def delete_coupon(request,id):
    coupon = Coupon.objects.get(id=id)
    coupon.delete()
    return redirect(offer_view)