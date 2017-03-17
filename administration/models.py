from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from bocatapp.models import User


# Create your models here.

class CreditCard(models.Model):
    name = models.CharField(max_length=32)
    expireMonth = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    expireYear = models.IntegerField(validators=[MinValueValidator(2017)])
    cvv = models.IntegerField(validators=[MinValueValidator(12), MaxValueValidator(999)])
    number = models.IntegerField()
    user = models.ForeignKey(User)

