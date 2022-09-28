from ast import Or
from statistics import mode
from tkinter import CASCADE
from urllib import request
from django.db import models
# Create your models here.
from django.contrib.auth.models import User
from products.models import Product
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    is_finished = models.BooleanField()
    details = models.ManyToManyField(Product, through='OrderDetails')
    total = 0
    count = 0
    def __str__(self):
        return self.user.username + ' ' + str(self.id)


class OrderDetails(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return self.order.user.username + ' ' + self.product.name + ' ' + str(self.id)

    class Meta:
        ordering = ['id']
class Payment(models.Model):
    order  = models.ForeignKey(Order , on_delete=models.CASCADE)
    shipment_address = models.CharField(max_length=150)
    shipment_phone = models.CharField(max_length=50)
    card_number = CardNumberField()
    expire = CardExpiryField()
    security_code = SecurityCodeField()