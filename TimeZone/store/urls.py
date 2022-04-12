

from django.urls import path
from . import views


urlpatterns = [
    
    path('',views.store, name='store'),
    path('product_details/<int:id>/',views.productDetails,name='product_details'),
    path('collections',views.collections,name='collections'),
    path('collections/<str:category_slug>',views.collectionsview,name='collectionsview'),
]
