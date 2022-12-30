from django.db import models


class Ads(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=1000)
    address = models.CharField(max_length=500)
    is_published = models.BooleanField(default=True)


class Categories(models.Model):
    name = models.CharField(max_length=50)
