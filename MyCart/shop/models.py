from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Customer(models.Model):
    user =models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,null=True)
    email= models.CharField(max_length=100,null=True)

    def __str__(self):
        if self.name!=None:
            return (self.name)
        return ''

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to='shop/images', default="")
    digital=models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return self.product_name

class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False,blank=True,null=True)
    transaction_id=models.CharField(max_length=200,null=True)
    order_id=models.AutoField(primary_key=True)

    def __str__(self):
        if(self.order_id>0):
            return str(self.order_id)
        return "ERROR"

    @property
    def shipping(self):
        shipping=False
        orderitem=self.orderitems_set.all()
        for i in orderitem:
            if i.product.digital==False:
                shipping=True
        return shipping

    @property
    def get_cart_total(self):
        orderitems=self.orderitems_set.all()
        total=sum([item.get_total for item in orderitems])
        return total

    def get_cart_item(self):
        orderitems = self.orderitems_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class Shippingaddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address=models.CharField(max_length=200,null=True)
    city= models.CharField(max_length=200,null=True)
    state=models.CharField(max_length=200,null=True)
    zip_code=models.CharField(max_length=200,null=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class OrderUpdate(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.IntegerField(default="")
    update_desc=models.CharField(max_length=5000)
    timestamp=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:10]+"..."


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,default=False)
    email = models.CharField(max_length=70, default=False)
    phone = models.CharField(max_length=70, default=False)
    description = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name