from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from bocatapp.models import User
from administration.services import CreditCardService


# Create your models here.

class CreditCard(models.Model):
    holderName = models.CharField(max_length=32)
    brandName = models.CharField(max_length=32)
    expireMonth = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    expireYear = models.IntegerField(validators=[MinValueValidator(2017)])
    cvv = models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(9999)])
    number = models.CharField(max_length=32,validators=[CreditCardService.luhn])
    user = models.ForeignKey(User)
    isDeleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.holderName

class Allergen(models.Model):
    name = models.CharField(max_length=32)
    icon = models.URLField(default="#")
    description = models.CharField(max_length=140)

    def __unicode__(self):
        return self.name
