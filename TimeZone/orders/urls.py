
from django.urls import path
from . import views


urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('order_view/<int:id>',views.order_view,name='order_view'),
    path('order_cancel_user/<int:order_number>',views.order_cancel_user,name='order_cancel_user'),
    path('return_order/<int:order_number>',views.return_order,name='return_order'),
    path('razor_success/',views.razor_success,name='razor_success'),
    path('cod<str:order_number>/',views.cash_on_delivery,name='cash_on_delivery'),
    path('paypal_complete/',views.paypal_complete,name='paypal_complete'),
    path('paypal_complete_display/',views.paypal_complete_display,name='paypal_complete_display'),
    

]
