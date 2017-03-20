from django.db import models
from seller.models import Local
from administration.models import CreditCard
from bocatapp.models import User
from seller.models import Product
from django.core.validators import MinValueValidator


# Create your models here.


class Order(models.Model):
    totalPrice = models.DecimalField(max_digits=4, decimal_places=2)
    moment = models.DateTimeField(auto_now=True)
    local = models.CharField(max_length=232)
    comment = models.CharField(max_length=232)
    customer = models.CharField(max_length=232)
    creditCard = models.CharField(max_length=232)
    status = models.NullBooleanField(default=None)
    pickupMoment = models.DateTimeField(auto_now=True)


class OrderLine(models.Model):
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class ShoppingCart(models.Model):
    customer = models.ForeignKey(User)


class ShoppingCartLine(models.Model):
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    product = models.ForeignKey(Product)
    shoppingCart = models.ForeignKey(ShoppingCart)