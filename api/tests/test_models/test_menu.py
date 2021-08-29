from django.test import TestCase

from api.models import Menu


class TestMenu(TestCase):
    def test_have_dishes(self):
        menu = Menu.objects.create()
        assert not menu.have_dishes
        menu.dishes.create(
            describe='test_describe',
            name='test_name',
            price='21.37',
            preparation_time='12:34',
            vegetarian=False,
        )
        assert menu.have_dishes
