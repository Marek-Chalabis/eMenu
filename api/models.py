from django.db import models
from djmoney.models.fields import MoneyField


class ProductABC(models.Model):
    describe = models.CharField(max_length=250)
    added_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Dish(ProductABC):
    name = models.CharField(max_length=50)
    price = MoneyField(max_digits=6, decimal_places=2, default_currency='EUR')
    preparation_time = models.TimeField()
    vegetarian = models.BooleanField()


class Menu(ProductABC):
    name = models.CharField(max_length=50, unique=True)
    dishes = models.ManyToManyField(Dish,related_name='menu', blank=True)
