from operator import mod
from django.db import models
from django.contrib.auth.models import User
from products.models import Product
# Create your models here.

class User_Profile(models.Model):
     user  =  models.OneToOneField(User,on_delete=models.CASCADE)
     product_fav = models.ManyToManyField(Product)
     address = models.CharField(max_length=60)
     address2 = models.CharField(max_length=60)
     city = models.CharField(max_length=60)
     state = models.CharField(max_length=60)
     zip_number = models.CharField(max_length=5)
     email = models.CharField(max_length=60)
     def __str__(self):
        return self.user.username