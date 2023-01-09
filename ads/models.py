from django.db import models
from django.db.models import CASCADE

from users.models import User


class Categories(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Ads(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=CASCADE, default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=1000)
    category = models.ForeignKey(Categories, on_delete=CASCADE, default=1)
    image = models.ImageField(upload_to='images/', default=None)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
