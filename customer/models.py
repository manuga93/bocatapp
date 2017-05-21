from django.db import models
from seller.models import Local
from administration.models import CreditCard
from bocatapp.models import User
from seller.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class PSCPayment(models.Model):
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    currency = models.CharField(max_length=25, default='EUR')
    serial = models.IntegerField()
    moment = models.DateTimeField(auto_now=True)
    customer_ip = models.CharField(max_length=25, blank=True)
    pysc_id = models.IntegerField()
    customer = models.ForeignKey(User)


class Order(models.Model):
    totalPrice = models.DecimalField(max_digits=4, decimal_places=2)
    moment = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=232)
    status = models.BooleanField(default=False)
    pickupMoment = models.DateTimeField(auto_now=True)
    hour = models.CharField(max_length=5)
    local = models.ForeignKey(Local)
    customer = models.ForeignKey(User)
    creditCard = models.ForeignKey(CreditCard, null=True)


class OrderLine(models.Model):
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name


class ShoppingCart(models.Model):
    customer = models.ForeignKey(User, blank=True, null=True)
    checkout = models.BooleanField(default=False)

    # Derivated property
    @property
    def total_price(self):
        return sum([line.product.price*line.quantity for line in self.shoppingcartline_set.all()])


class ShoppingCartLine(models.Model):
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    product = models.ForeignKey(Product)
    shoppingCart = models.ForeignKey(ShoppingCart)


class Comment(models.Model):
    description = models.CharField(max_length=256)
    rating = models.CharField(max_length=1)
    reported = models.BooleanField(default=False)
    local = models.ForeignKey(Local)
    customer = models.ForeignKey(User)


class Report(models.Model):
    customer = models.ForeignKey(User)
    reason = models.CharField(max_length=256)
    accepted = models.BooleanField(default=False)
    decline = models.BooleanField(default=False)
    comment = models.ForeignKey(Comment)
