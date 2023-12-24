from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient


class TrainerTestCase(TestCase):
    url = reverse('trainer-list')

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_trainer(self):
        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 0

        trainer_name = 'qwe'
        response = self.client.post(self.url, data={'full_name': trainer_name})
        trainer_data = response.json()
        assert response.status_code == 201

        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 1

        response = self.client.get(f"{self.url}{trainer_data['id']}/")
        data = response.json()
        assert data['full_name'] == trainer_name

    def test_delete_trainer(self):
        response = self.client.post(self.url, data={'full_name': 'qwe'})
        trainer_id = response.json()['id']

        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 1

        self.client.delete(f"{self.url}{trainer_id}/")
        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 0

    def test_update_trainer(self):
        trainer_name = 'qwe'
        response = self.client.post(self.url, data={'full_name': trainer_name})
        trainer_id = response.json()['id']

        response = self.client.get(f"{self.url}{trainer_id}/")
        data = response.json()
        assert data['full_name'] == trainer_name

        new_trainer_name = 'asd'
        response = self.client.patch(f"{self.url}{trainer_id}/", data={'full_name': new_trainer_name})
        data = response.json()
        assert data['full_name'] == new_trainer_name

        new_trainer_name = 'zxc'
        response = self.client.put(f"{self.url}{trainer_id}/", data={'full_name': new_trainer_name})
        data = response.json()
        assert data['full_name'] == new_trainer_name
