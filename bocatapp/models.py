from django.db import models
from django.contrib.auth.models import AbstractUser

default = "http://s3.amazonaws.com/37assets/svn/765-default-avatar.png"


class User(AbstractUser):
    amount_money = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    phone = models.CharField(max_length=14)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.URLField(default=default)

    class Meta:
        db_table = 'auth_user'
        permissions = (('customer', 'Customer'), ('seller', 'Seller'))
