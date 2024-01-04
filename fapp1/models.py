from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.
class CustomUser(AbstractUser):
   
    user_type = models.CharField(default=1, max_length=10)
    
class Client(models.Model):
   
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True) 
    age=models.IntegerField()
    number=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    photo=models.FileField(upload_to='image/',null=True)
    tracking_id=models.CharField(max_length=255,null=True)
    location=models.TextField(null=True) 
    
    
  
    
class Delivery(models.Model): 
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True) 
    number=models.CharField(max_length=255)
    image=models.ImageField(upload_to='image/',null=True,blank=True)
    
class Delivery1(models.Model): 
    user_type=models.CharField(default=2, max_length=10)
    number=models.CharField(max_length=255,null=True) 
    image=models.ImageField(upload_to='image/',null=True,blank=True)
    first_name=models.CharField(max_length=255,null=True)
    last_name=models.CharField(max_length=255,null=True)
    username=models.CharField(max_length=255,null=True) 
    email=models.EmailField(null=True)
    address=models.CharField(max_length=255,null=True)
    delivery=models.BooleanField(default=False)
    client=models.BooleanField(default=False)
    is_approved=models.BooleanField(default=False) 
    
class Notification (models.Model):
    sender=models.ForeignKey(Delivery1,on_delete=models.CASCADE,null=True)
    message=models.TextField()
    is_read = models.BooleanField(default=False)
    
class Product(models.Model):
    name=models.CharField(max_length=40,null=True)
    pimage= models.ImageField(upload_to='image/',null=True,blank=True)
    price = models.PositiveIntegerField(null=True)
    description=models.CharField(max_length=40,null=True)
    qty = models.PositiveIntegerField(null=True) 
    def __str__(self):
        return self.name

class Orders(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('In Transist','In Transist'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    client=models.ForeignKey('Client', on_delete=models.CASCADE,null=True)
    product=models.ForeignKey('Product',on_delete=models.CASCADE,null=True)
    email = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=500,null=True)
    mobile = models.CharField(max_length=20,null=True) 
    order_date= models.DateField(auto_now_add=True,null=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)
    deliveryboy=models.ForeignKey(Delivery,on_delete=models.CASCADE,null=True) 
    tracking_id=models.CharField(max_length=255,null=True) 
    is_receive=models.CharField(max_length=255,null=True)
    is_delivered=models.BooleanField(default=False) 
    place = models.CharField(max_length=50,null=True)
    noofitems=models.IntegerField(null=True) 
    deliverymethod=models.CharField(max_length=50,null=True)
    
    
class Cart(models.Model):
    customer=models.ForeignKey(Client, on_delete=models.CASCADE,null=True)
    products=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField(default=1)

