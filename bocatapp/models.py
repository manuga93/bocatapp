from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    amount_money = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    class Meta:
        db_table = 'auth_user'
        permissions = (('customer', 'Customer'), ('seller', 'Seller'))


default = "http://s3.amazonaws.com/37assets/svn/765-default-avatar.png"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=14)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.URLField(default=default)

    def __unicode__(self):
        return self.user.username
