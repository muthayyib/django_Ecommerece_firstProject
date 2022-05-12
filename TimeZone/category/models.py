from distutils.command.upload import upload
from tabnanny import verbose
from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    category_slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=225, blank=True)
    cat_img = models.ImageField(upload_to='photos/category', blank = True)
   
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name
    
