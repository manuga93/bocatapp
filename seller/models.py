from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=48)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    category = models.ManyToManyField(Category)

    def __unicode__(self):
        return self.name


class Local(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    address = models.CharField(max_length=55)
    phone = models.CharField(max_length=12)
    photo = models.URLField()
    isActive = models.BooleanField(default=True)
    seller = models.ForeignKey(User)
    products = models.ForeignKey(Product)

    def __unicode__(self):
        return self.name






