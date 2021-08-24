from django.db import models
from djmoney.models.fields import MoneyField


class Dish(models.Model):
    name = models.CharField(max_length=50)
    describe = models.CharField(max_length=250)
    price = MoneyField(max_digits=6, decimal_places=2, default_currency='EUR')
    preparation_time = models.TimeField()
    added_date = models.DateField()
    modified_date = models.DateField
    vegetarian = models.BooleanField()


class Menu(models.Model):
    name = models.CharField(max_length=50, unique=True)
    describe = models.CharField(max_length=250)
    added_date = models.DateField()
    modified_date = models.DateField
    dishes = models.ManyToManyField(Dish)