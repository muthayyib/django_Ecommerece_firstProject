from django.urls import path
from . import views


urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:product_id>/',views.remove_cart,name='remove_cart'),
    path('delete_item/<int:product_id>/',views.delete_item,name='delete_item'),
    path('checkout/',views.checkout,name='checkout'),
    path('coupon_apply/',views.coupon_apply,name='coupon_apply'),
]
