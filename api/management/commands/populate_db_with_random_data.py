import uuid


from typing import List
import random

from django.contrib.auth.models import User
from django.core.management import BaseCommand
import requests

from api.models import Dish, Menu
from api.tests.test_utils import get_random_date


class Command(BaseCommand):
    help = 'Populate DB with random data'

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            '--users', type=int, default=20, help='Number of users to generate'
        )
        parser.add_argument(
            '--dishes',
            type=int,
            default=60,
            help='Number of dishes to generate',
        )
        parser.add_argument(
            '--menus', type=int, default=20, help='Number of menus to generate'
        )

    def handle(self, *args, **options) -> None:
        users_number = options['users']
        dishes_number = options['dishes']
        menus_number = options['menus']
        users = self._create_users(users_number)
        dishes = self._create_dishes(dishes_number=dishes_number, users=users)
        self._create_menus(
            menus_number=menus_number, users=users, dishes=dishes
        )

    def _create_users(self, users_number: int) -> List[User]:
        """Returns created users."""
        random_user_data = requests.get(
            f'https://randomuser.me/api/?results={users_number}'
        ).json()['results']
        users_data = [
            User(
                username=user_data['login']['username'],
                password=user_data['login']['password'],
                email=user_data['email'],
            )
            for user_data in random_user_data
        ]
        return User.objects.bulk_create(users_data)

    def _create_dishes(
        self, dishes_number: int, users: List[User]
    ) -> List[Dish]:
        """Returns created dishes."""
        created = get_random_date()
        modified = get_random_date(start_date=created)
        dishes = [
            requests.get(
                'https://www.themealdb.com/api/json/v1/1/random.php'
            ).json()['meals'][0]
            for _ in range(dishes_number)
        ]
        dishes_data = [
            Dish(
                name=dish['strMeal'][:50],
                describe=dish['strInstructions'][:250],
                created=created,
                created_by=random.choice(users),
                modified=modified,
                modified_by=random.choice(users),
                price=random.randint(10000, 99999) / 100.00,
                preparation_time=f'{random.randint(1, 30)}:{random.randint(0, 59)}',
                vegetarian=random.choice([True, False]),
            )
            for dish in dishes
        ]
        return Dish.objects.bulk_create(dishes_data)

    def _create_menus(
        self, menus_number: int, users: List[User], dishes: List[Dish]
    ) -> None:
        created = get_random_date()
        modified = get_random_date(start_date=created)
        menus_data = [
            Menu(
                name=f'test_menu{uuid.uuid4()}',
                describe=requests.get(
                    'https://loripsum.net/api/10/short/plaintext'
                ).content[:200],
                created=created,
                created_by=random.choice(users),
                modified=modified,
                modified_by=random.choice(users),
            )
            for _ in range(menus_number)
        ]
        menus = Menu.objects.bulk_create(menus_data)
        dishes_pk = [dish.pk for dish in dishes]
        for menu in menus:
            menu.dishes.add(*random.sample(dishes_pk, random.randint(0, 10)))
