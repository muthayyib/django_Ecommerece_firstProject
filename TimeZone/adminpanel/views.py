import os
from socket import IPV6_DONTFRAG
from django.contrib import messages
from django.shortcuts import redirect, render
from pkg_resources import get_default_cache
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
    return render (request,'admin_panel/dashboard_adm.html')

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




    
    