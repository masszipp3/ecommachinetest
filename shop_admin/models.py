from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_shopadmin = models.BooleanField(default=False)
    is_customer=models.BooleanField(default=False)

class Accounts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True)
    contact_number = models.CharField(max_length=20,null=True)
    profile_pic = models.ImageField(upload_to="accounts/",null=True)

class Address(models.Model):
    Account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    recipient_name = models.CharField(max_length=100)
    apartment_suite = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.recipient_name}, {self.street_address}, {self.city}, {self.state} {self.postal_code}, {self.country}"  


class Categories(models.Model):    
    category_name=models.CharField(max_length=50)
    category_ID=models.CharField(max_length=20,null=False)
    category_image=models.ImageField(upload_to="customer/",null=True)
    category_description=models.TextField(null=True)
    slug=models.CharField(max_length=50,null=False)

class Product(models.Model):
    Product_name=models.CharField(max_length=40)
    Product_ID=models.CharField(max_length=20,unique=True,db_index=True)
    slug=models.CharField(max_length=50,null=True,unique=True)
    brand=models.CharField(max_length=30, default='Ecom_Test')
    Min_value=models.CharField(max_length=50)
    Product_category=models.ForeignKey(Categories,on_delete=models.CASCADE)
    onstock=models.BooleanField(default=True)
    Price=models.FloatField()
    Description=models.TextField(null=True)
    created_at= models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    product_image=models.ImageField(upload_to="shopadmin/",null=True)

class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Accounts,on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.CharField(max_length=200, null=True)