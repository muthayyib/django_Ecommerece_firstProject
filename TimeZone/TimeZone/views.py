from itertools import product
from django.shortcuts import render
from category.models import Category
from store.models import Product




#set home view

def home(request):
    products = Product.objects.filter(is_available=True)
    category = Category.objects.all()
    context= {
        'products':products,
        'category':category,
    }
    return render(request, 'index.html',context)