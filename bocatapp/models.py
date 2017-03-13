from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    phone = models.CharField(max_length = 14)
    photo = models.URLField()
    user = models.OneToOneField(User)