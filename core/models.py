from django.db import models 
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    middle_name = models.CharField(max_length=250, blank=True, null= True)
    last_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=100, choices=[('Male','Male'),('Female','Female')], blank=True, null= True)
    dob = models.DateField(blank=True, null= True)
    contact = models.CharField(max_length=250, blank=True, null= True)
    address=models.CharField(max_length=250, blank=True, null= True)
    country=models.CharField(max_length=250, blank=True, null= True)
    city=models.CharField(max_length=250, blank=True, null= True)
    zipcode=models.IntegerField(blank=True, null= True)
    status=models.IntegerField(default=1)
    avatar = models.ImageField(upload_to= 'images/')
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

category_choice=(
    ('Mens Dresses','Mens Dresses'),
    ('Women Dresses','Women Dresses'),
    ('Baby Dresses','Baby Dresses')
)  
class category(models.Model):
    name=models.CharField(max_length=250, blank=True, null= True)
    description=models.CharField(max_length=250, blank=True, null= True)
    category_type=models.CharField(max_length=250, blank=True, choices=category_choice)

size_choice=(
    ('XL','XL'),
    ('L','L'),
    ('M','M'),
    ('S','S')
)  
 
class Product(models.Model):
    categori=models.ForeignKey(category,on_delete=models.CASCADE)
    name=models.CharField(max_length=250, blank=True, null= True)
    price = models.FloatField(max_length=30)
    discounted_price = models.FloatField(max_length=20)
    productcolor=models.CharField(max_length=30,)
    product_size=models.CharField(max_length=50,choices=size_choice)
    descrption = models.TextField()
    brand = models.CharField(max_length=20,default='Diner')
    product_img = models.ImageField(upload_to='images/')

order_status =(
    ('accepted','accepted'),
    ('on the way','on the way'),
    ('Dileverd','Dileverd'),
    ('cancel','cancel'),
)
class palceorder(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    order_date=models.DateField(default=timezone.now)
    status = models.CharField(choices=order_status,max_length=20,default='pending') 


class cart(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,default=None)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

class Comment(models.Model):
    title = models.CharField(max_length=255,null=True,blank=True)
    content = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', related_query_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', related_query_name='comment')
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='comments', related_query_name='comment')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    rate=models.IntegerField(default=1)

    def __str__(self):
        return self.title

class wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiel')
    created = models.DateField(auto_now_add=True)