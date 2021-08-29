from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from api.models import Menu, Dish


class UtilsMixinAPITestCase:
    def set_authorization_user_token(self):
        user = User.objects.create_user(
            username="test_user", password='test_passwrod'
        )
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    def create_menu(self, menu_name='test_menu', number_of_dishes=0) -> Menu:
        menu = Menu.objects.create(name=menu_name)
        for _ in range(number_of_dishes):
            menu.dishes.add(self.create_dish())
        return menu

    def create_dish(self) -> Menu:
        return Dish.objects.create(
            describe="test_describe",
            name="test_name",
            price="21.37",
            preparation_time="12:34",
            vegetarian=False,
        )
