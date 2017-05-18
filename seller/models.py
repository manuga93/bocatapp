from django.core.exceptions import ValidationError
from django.db import models
from bocatapp.models import User

# Create your models here.


class Local(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    address = models.CharField(max_length=55)
    phone = models.CharField(max_length=12)
    photo = models.URLField(blank=True)
    isActive = models.BooleanField(default=True)
    postalCode = models.PositiveIntegerField()
    seller = models.ForeignKey(User)
    avg_rating = models.DecimalField(max_digits=3 , decimal_places=2, default=0.)

    def __unicode__(self):
        return self.name


class LocalCategory(models.Model):
    name = models.CharField(max_length=32)
    locals = models.ManyToManyField(Local, related_name="locals")

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    local = models.ForeignKey(Local)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=48)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    ingredients = models.CharField(max_length=256, default="Ingrediente")
    category = models.ForeignKey(Category, null=True)
    local = models.ForeignKey(Local)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class ProductLine(models.Model):
    quantity = models.PositiveSmallIntegerField()
    # Relationships
    product = models.ForeignKey(Product)
    pack = models.ForeignKey('Pack', on_delete=models.CASCADE)


class Pack(models.Model):
    name = models.CharField(max_length=140)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    initDate = models.DateField(auto_now=True)
    endDate = models.DateField()
    deleted = models.BooleanField(default=False)
    photo = models.URLField(default='/static/images/No_image_available.png')
    # Relationships
    local = models.ForeignKey(Local)
