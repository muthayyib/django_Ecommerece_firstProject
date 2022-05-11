from calendar import c
from django.db import models
from store.models import Product
from accounts.models import Account
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=50,blank=True)
    date_added = models.DateTimeField(auto_now_add =True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def item_total(self):
        return self.product.price * self.quantity


    def __str__(self):
        return self.product.product_name


#model for coupons

class Coupon(models.Model):
    code = models.CharField(max_length=50,unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.code

    def discount_amount(self,sub_total):
        return self.discount/100*sub_total

class CouponUsedUser(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    count =models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return self.user.user_name