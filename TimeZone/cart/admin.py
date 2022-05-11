from django.contrib import admin
from . models import Cart,CartItem,Coupon,CouponUsedUser

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)

class CouponAdmin(admin.ModelAdmin):
    list_display =['code','valid_from','valid_to','discount']
    list_filter = ['active']
    search_fields = ['code']

admin.site.register(Coupon,CouponAdmin)
admin.site.register(CouponUsedUser)