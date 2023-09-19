from django.db import models
from shop_admin.models import Product,Categories,Accounts,User,Address

# Create your models here.  

class Cart(models.Model):
    customer = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartItem')

    def total_price(self):
        return sum(item.subtotal() for item in self.cartitem_set.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    STATUS_CHOICES = (
        ('approved', 'Approved'),
        ('shipped', 'Shipped'),
        ('delvired', 'Delivered'),
    )


    OrderId=models.CharField(max_length=20,null=True,unique=True)
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    paymentmethod=models.CharField(max_length=4,default='COD')
    address= models.ForeignKey(Address, on_delete=models.CASCADE ,default='')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)



    