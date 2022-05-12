from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from category.models import Category
from store.models import Product

class CategoryOffer(models.Model):
    
    # now = datetime.date.today()

    category = models.OneToOneField(Category,related_name='cat_offer',on_delete=models.CASCADE)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.category.category_name

    def discount_amount(self,sub_total):
        return self.discount/100*sub_total

class ProductOffer(models.Model):
    product = models.OneToOneField(Product,related_name='pro_offer',on_delete=models.CASCADE)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.product.product_name

    def discount_amount(self,sub_total):
        return self.discount/100*sub_total

