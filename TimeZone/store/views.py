
import django
from django.shortcuts import redirect, render
from .models import Product
from category.models import Category
from django.contrib import messages
# Create your views here.
def store(request):
    products = Product.objects.all().filter(is_available =True)
    product_count = products.count()

    context = {
        'products':products,
        'count': product_count
    }
    return render (request,'store.html',context)


# product view based on category 
def collections(request):
    category = Category.objects.filter(status=0)
    print(category)
    context = {
        'category':category
    }
    return render(request,'store/collections.html',context)

#collections viewy
def collectionsview(request,category_slug):
    if(Category.objects.filter(category_slug=category_slug,status=0)):
        product = Product.objects.filter(category__category_slug=category_slug)
        category = Category.objects.filter(category_slug=category_slug).first()
        context  ={
            'product':product,'category':category
        }
        return render(request,'store/product_by_category.html',context)
    else:
        messages.warning(request,'No match found')
        return redirect('collections')

#product deatiled view for user
def productDetails(request,cat_slug,prod_slug):
    if(Category.objects.filter(category_slug=cat_slug,status=0)):
        if(Product.objects.filter(product_slug=prod_slug,status=0)):
            product = Product.objects.filter(product_slug=prod_slug,status=0).first()
            context = {'product':product}
    
        else:
            messages.error(request,'No such products')
            return redirect('collections')

    else:
        messages.error(request,'No such category')
        return redirect('collections')
    return render(request, 'store/view_pro.html',context)
