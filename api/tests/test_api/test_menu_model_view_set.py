from unittest.mock import patch, PropertyMock

from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.test_api.test_utils import UtilsMixinAPITestCase


class TestMenuModelViewSet(UtilsMixinAPITestCase, APITestCase):
    def test_create_without_dish(self):
        self.set_authorization_user_token()
        response = self.client.post(
            path='/api/v1/menus/',
            data={
                "describe": "test_menu",
                "name": "test_menu",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_with_dish(self):
        self.set_authorization_user_token()
        test_dish = self.create_dish()
        response = self.client.post(
            path='/api/v1/menus/',
            data={
                **{
                    "describe": "test_menu",
                    "name": "test_menu",
                },
                "dishes": [test_dish.id],
            },
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_un_authorization_access(self):
        response = self.client.post(path='/api/v1/menus/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_authorization_with_dish(self):
        self.set_authorization_user_token()
        test_menu = self.create_menu(number_of_dishes=1)
        response = self.client.get(path=f'/api/v1/menus/{test_menu.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_authorization_without_dish(self):
        self.set_authorization_user_token()
        test_menu = self.create_menu()
        response = self.client.get(path=f'/api/v1/menus/{test_menu.id}/')
        assert response.status_code == status.HTTP_200_OK

    @patch(
        'api.models.Menu.have_dishes',
        new_callable=PropertyMock,
        return_value=True,
    )
    def test_retrieve_un_authorization_with_dish(self, mock_have_dishes):
        test_menu = self.create_menu()
        response = self.client.get(path=f'/api/v1/menus/{test_menu.id}/')
        assert response.status_code == status.HTTP_200_OK

    @patch(
        'api.models.Menu.have_dishes',
        new_callable=PropertyMock,
        return_value=True,
    )
    def test_retrieve_un_authorization_with_dish_show_dishes(
        self, mock_have_dishes
    ):
        test_menu = self.create_menu()
        response = self.client.get(path=f'/api/v1/menus/{test_menu.id}/')
        assert response.status_code == status.HTTP_200_OK

    @patch(
        'api.models.Menu.have_dishes',
        new_callable=PropertyMock,
        return_value=False,
    )
    def test_retrieve_un_authorization_without_dish(self, mock_have_dishes):
        test_menu = self.create_menu()
        response = self.client.get(path=f'/api/v1/menus/{test_menu.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_changed_data(self):
        self.set_authorization_user_token()
        test_menu = self.create_menu(number_of_dishes=1)
        response = self.client.get(path=f'/api/v1/menus/{test_menu.id}/')
        assert {
            "describe": "test_describe",
            "name": "test_name",
            "price": "21.37",
            "vegetarian": False,
        }.items() <= response.json()['dishes'][0].items()
        assert '12:34:00' == response.json()['dishes'][0]['preparation_time']

    def test_list(self):
        self.set_authorization_user_token()
        response = self.client.get(path='/api/v1/menus/')
        assert response.status_code == status.HTTP_200_OK

    def test_list_un_authorization_access(self):
        response = self.client.get(path='/api/v1/menus/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_menus_with_dishes(self):
        self.create_menu(number_of_dishes=1)
        self.create_menu(menu_name='test_name_2')
        response = self.client.get(path='/api/v1/menus/menus_with_dishes/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['results']) == 1

    def test_update_put(self):
        self.set_authorization_user_token()
        test_menu = self.create_menu()

        put_response = self.client.put(
            path=f'/api/v1/menus/{test_menu.id}/',
            data={
                "describe": "test_describe_put",
                "name": "test_menu",
            },
        )
        assert put_response.status_code == status.HTTP_200_OK
        test_menu_json_put = put_response.json()
        assert test_menu_json_put['describe'] != test_menu.describe

    def test_put_un_authorization_access(self):
        test_menu = self.create_menu()
        response = self.client.put(path=f'/api/v1/menus/{test_menu.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_patch(self):
        self.set_authorization_user_token()
        test_menu = self.create_menu()
        patch_response = self.client.patch(
            path=f'/api/v1/menus/{test_menu.id}/',
            data={"describe": "test_describe_put"},
        )
        assert patch_response.status_code == status.HTTP_200_OK
        test_menu_json_put = patch_response.json()
        assert test_menu_json_put['describe'] != test_menu.describe

    def test_patch_un_authorization_access(self):
        test_menu = self.create_menu()
        response = self.client.patch(path=f'/api/v1/menus/{test_menu.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
