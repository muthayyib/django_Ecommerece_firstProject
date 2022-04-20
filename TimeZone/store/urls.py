

from django.urls import path
from . import views


urlpatterns = [
    
    path('',views.store, name='store'),
    
    path('collections',views.collections,name='collections'),
    path('collections/<str:category_slug>',views.collectionsview,name='collectionsview'),
    path('collections/<str:cat_slug>/<str:prod_slug>',views.productDetails,name='product_details'),
]
