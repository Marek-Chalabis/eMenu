from api.tests.test_api.test_utils import UtilsMixinAPITestCase

import io

from PIL import Image

from rest_framework import status
from rest_framework.test import APITestCase


class TestDishModelViewSet(UtilsMixinAPITestCase, APITestCase):
    def test_create(self):
        self.set_authorization_user_token()
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        response = self.client.post(
            path='/api/v1/dishes/',
            data={
                'describe': 'test_describe',
                'name': 'test_name',
                'price': '21.37',
                'preparation_time': '12:34',
                'vegetarian': False,
                'image': file,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_read_only_fields(self):
        self.set_authorization_user_token()
        response_json = self.client.post(
            path='/api/v1/dishes/',
            data={
                'describe': 'test_describe',
                'name': 'test_name',
                'price': '21.37',
                'preparation_time': '12:34',
                'vegetarian': False,
                'modified': 'test_modified',
                'created': 'test_created',
            },
        ).json()
        assert response_json['modified'] != 'test_modified'
        assert response_json['created'] != 'test_created'

    def test_create_un_authorization_access(self):
        response = self.client.post(path='/api/v1/dishes/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve(self):
        self.set_authorization_user_token()
        test_dish = self.create_dish()
        response = self.client.get(path=f'/api/v1/dishes/{test_dish.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_fields(self):
        self.set_authorization_user_token()
        test_dish = self.create_dish()
        response = self.client.get(path=f'/api/v1/dishes/{test_dish.id}/')
        assert list(response.json().keys()) == [
            'name',
            'describe',
            'created',
            'modified',
            'price',
            'preparation_time',
            'vegetarian',
            'image',
        ]

    def test_retrieve_un_authorization_access(self):
        response = self.client.get(path='/api/v1/dishes/1/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list(self):
        self.set_authorization_user_token()
        response = self.client.get(path='/api/v1/dishes/')
        assert response.status_code == status.HTTP_200_OK

    def test_list_un_authorization_access(self):
        response = self.client.get(path='/api/v1/dishes/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_put(self):
        self.set_authorization_user_token()
        test_dish = self.create_dish()
        put_response = self.client.put(
            path=f'/api/v1/dishes/{test_dish.id}/',
            data={
                'describe': 'test_describe_put',
                'name': 'test_name',
                'price': '21.37',
                'preparation_time': '12:34',
                'vegetarian': False,
            },
        )
        assert put_response.status_code == status.HTTP_200_OK
        test_dish_json_put = put_response.json()
        assert test_dish_json_put['describe'] != test_dish.describe

    def test_put_un_authorization_access(self):
        test_dish = self.create_dish()
        response = self.client.put(path=f'/api/v1/dishes/{test_dish.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_patch(self):
        self.set_authorization_user_token()
        test_dish = self.create_dish()
        patch_response = self.client.patch(
            path=f'/api/v1/dishes/{test_dish.id}/',
            data={'describe': 'test_describe_put'},
        )
        assert patch_response.status_code == status.HTTP_200_OK
        test_dish_json_put = patch_response.json()
        assert test_dish_json_put['describe'] != test_dish.describe
        assert test_dish_json_put['describe'] == 'test_describe_put'

    def test_patch_un_authorization_access(self):
        test_dish = self.create_dish()
        response = self.client.patch(path=f'/api/v1/dishes/{test_dish.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
