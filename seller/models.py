from django.core.exceptions import ValidationError
from django.db import models
from bocatapp.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)

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

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=48)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    category = models.ManyToManyField(Category)
    # local = models.CharField(max_length=48)
    local = models.ForeignKey(Local)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class ProductLine(models.Model):
    quantity = models.PositiveSmallIntegerField()
    # Relationships
    product = models.ForeignKey(Product)
    pack = models.ForeignKey('Pack')


class Pack(models.Model):
    name = models.CharField(max_length=140)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    initDate = models.DateField(auto_now=True)
    endDate = models.DateField()
    deleted = models.BooleanField(default=False)
    # Relationships
    local = models.ForeignKey(Local)

    def clean(self):
        if self.initDate > self.endDate:
            raise ValidationError('Start date is after end date')
