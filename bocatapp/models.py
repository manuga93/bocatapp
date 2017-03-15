from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'
        permissions = (('customer', 'Customer'), ('seller', 'Seller'))


class Profile(models.Model):
    phone = models.CharField(max_length=14)
    photo = models.URLField()
    user = models.OneToOneField(User)
