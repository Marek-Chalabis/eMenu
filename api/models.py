from django.db import models
from djmoney.models.fields import MoneyField
from crum import get_current_user


class ProductABC(models.Model):
    describe = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        'auth.User',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='%(class)s_created_by',
    )
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        'auth.User',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='%(class)s_modified_by',
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super().save(*args, **kwargs)


class Dish(ProductABC):
    name = models.CharField(max_length=50)
    price = MoneyField(max_digits=6, decimal_places=2, default_currency='EUR')
    preparation_time = models.TimeField()
    vegetarian = models.BooleanField()
    image = models.ImageField(upload_to='dish_images', null=True)


class Menu(ProductABC):
    name = models.CharField(max_length=50, unique=True)
    dishes = models.ManyToManyField('Dish', related_name='menus', blank=True)

    @property
    def have_dishes(self) -> bool:
        return bool(self.dishes.filter(pk=self.pk).exists())
