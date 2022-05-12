import email
from pickle import TRUE
from sre_parse import State
from django.db import models
from accounts.models import Account
from store.models import Product
from cart.models import Coupon
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Payment(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )
    user = models.ForeignKey(Account,on_delete=models.CASCADE, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned')

    )
    PAYMENT_MODE = (
        ('COD','COD'),
        ('PAYPAL','PAYPAL'),
        ('RAZOR_PAY','RAZORPAY')
    )
    user = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True, null=TRUE)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50,blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=10, null=True, blank=True)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(max_length=20,blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    coupon  = models.ForeignKey(Coupon,related_name='orders',on_delete=models.CASCADE,null=True,blank=True)
    discount = models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(50)])

    def __str__(self):
        return self.first_name

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line1} {self.address_line2}'

    def __str__(self):
        return self.first_name
    class Meta:
        ordering = ['-created_at','-updated_at']

class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField() 
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def sub_total(self):
        return self.product_price * self.quantity

    

    def __str__(self):
        return self.product.product_name

    class Meta:
        ordering= ('-created_at','-updated_at')

class RazorPay(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    razor_pay = models.CharField(max_length=200)
    
    def __str__(self):
        return self.order.order_number

