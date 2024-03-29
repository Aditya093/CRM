from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
# Create your models here.
def add_custom_fields_to_user():
    # Add custom fields to the User model
    User.add_to_class('reset_token' ,models.CharField(max_length=100, null=True, blank=True))
    
add_custom_fields_to_user()    
        
class Customer(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    profile_pic=models.ImageField(default='default.png',null=True,blank=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name 
class Tag(models.Model):
    
    name=models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name          
class Product(models.Model):   
    CATEGORY=(
        ('Indoor','Indoor'),
        ('Out Door','Out Door'),
    ) 
  
    name=models.CharField(max_length=200,null=True,unique=True)
    price=models.FloatField(null=True,unique=True)
    category=models.CharField(max_length=200,null=True,choices=CATEGORY)
    description=models.CharField(max_length=200,null=True,blank=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    tags=models.ManyToManyField(Tag)   
    
    def __str__(self):
            return self.name 

  
class Order(models.Model):
    STATUS=(
        ('Pending','Pending'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
        
    )
   
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    ordered_price =models.FloatField(null=True)
    date_created= models.DateTimeField(auto_now_add=True,null=True)
    status=models.CharField(max_length=200,null=True,choices=STATUS)
    note=models.CharField(max_length=500,null=True)
    def __str__(self):
        return self.product.name 
     
    