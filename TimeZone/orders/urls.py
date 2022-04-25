
from django.urls import path
from . import views


urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('order_view/<int:id>',views.order_view,name='order_view'),
    path('order_cancel_user/<int:order_number>',views.order_cancel_user,name='order_cancel_user'),
]
