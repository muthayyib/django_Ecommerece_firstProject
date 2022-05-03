"""TimeZone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from unicodedata import name
from . import views
from django.urls import path

urlpatterns = [
 
    path('',views.login_admin, name='login_admin'),
    path('logout_admin',views.logout_admin,name='logout_admin'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('users_adm/',views.users_adm, name='users_adm'),
    path('user_detail/<int:id>',views.user_detail,name='user_detail'),
    path('acivateUser/<int:id>',views.activateUser,name='activate_user'),
  
    path('deactivateUser/<int:id>',views.deactivateUser,name='deactivate_user'),
    path('product_view/',views.product_view,name='product_view'),
    path('add_product',views.add_product,name='add_product'),
    path('edit_product/<int:id>',views.edit_product,name='edit_product'),
    path('delete_product/<int:id>',views.delete_product,name='delete_product'),
    path('category_view/',views.category_view,name='category_view'),
    path('add_category',views.add_category,name="add_category"),
    path('edit_category/<int:id>',views.edit_category,name='edit_category'),
    path('delete_category/<int:id>',views.delete_category,name='delete_category'),
    path('order_manage/', views.order_manage,name='order_manage'),
    path('order_cancel/<int:order_number>',views.order_cancel,name='order_cancel'),
    path('change_status/<int:order_number>',views.change_status,name='change_status'),  
    path('export_csv',views.export_csv,name='export_csv'),
    path('export_excel',views.export_excel,name='export_excel'),
    path('export_pdf',views.export_pdf,name='export_pdf'),
    
]
