from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class FeatureProduct(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    desc=models.CharField(max_length=300)
    price = models.IntegerField()
    image = models.ImageField(upload_to='product',default="")

    def __str__(self):
        return self.product_name 

class Category(models.Model):
    slug = models.CharField(max_length=150, null = False,blank = False)
    name = models.CharField(max_length=150, null = False,blank = False)
    image = models.ImageField(upload_to='category',default="")
    description = models.TextField(max_length=250, null = False,blank = False)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.CharField(max_length=150, null = False,blank = False)
    name = models.CharField(max_length=150, null = False,blank = False)
    product_image = models.ImageField(upload_to='cat_product',default="")
    small_description = models.CharField(max_length=250, null=False, blank=False)
    quantity = models.IntegerField(null = False,blank = False)
    description = models.TextField(max_length=500, null = False,blank = False)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")
    new_arrival = models.BooleanField(default=False, help_text="0=default, 1=NEW")
    price = models.IntegerField()
    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)

    