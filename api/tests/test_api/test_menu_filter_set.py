from datetime import datetime

from rest_framework.test import APITestCase

from api.tests.test_api.test_utils import UtilsMixinAPITestCase


class TestMenuFilterSet(UtilsMixinAPITestCase, APITestCase):
    def setUp(self):
        self.url = '/api/v1/menus/menus_with_dishes/?'
        self.create_menu(menu_name='test_menu_1', number_of_dishes=1)
        self.create_menu(menu_name='test_menu_2', number_of_dishes=2)

    def test_filter_by_name(self):
        response = self.client.get(path=f'{self.url}name=test_menu_1')
        assert response.json()['count'] == 1

    def test_filter_by_dishes_count(self):
        response = self.client.get(path=f'{self.url}dishes_count=1')
        assert response.json()['count'] == 1

    def test_filter_by_created(self):
        now = datetime.now()
        response = self.client.get(path=f'{self.url}created__gt={now}')
        assert response.json()['count'] == 0
        response = self.client.get(path=f'{self.url}created__lt={now}')
        assert response.json()['count'] == 2

    def test_filter_by_modified(self):
        now = datetime.now()
        response = self.client.get(path=f'{self.url}modified__gt={now}')
        assert response.json()['count'] == 0
        response = self.client.get(path=f'{self.url}modified__lt={now}')
        assert response.json()['count'] == 2
