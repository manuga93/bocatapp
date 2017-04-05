from django.db import models
from seller.models import Local
from administration.models import CreditCard
from bocatapp.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


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


class ShoppingCartLine(models.Model):
    quantity = models.IntegerField(validators=[MinValueValidator(1)])


class ShoppingCart(models.Model):
    customer = models.ForeignKey(User)
    shoppingCartLine = models.ForeignKey(ShoppingCartLine)


class Comment(models.Model):
    description = models.CharField(max_length=256)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    reported = models.BooleanField(default=False)
    local = models.ForeignKey(Local)
    customer = models.ForeignKey(User)


class Report(models.Model):
    reason = models.CharField(max_length=256)
    accepted = models.BooleanField(default=False)
    decline = models.BooleanField(default=False)
    comment = models.ForeignKey(Comment)
