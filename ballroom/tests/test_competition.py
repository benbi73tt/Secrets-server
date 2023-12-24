from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient


class CompetitionTestCase(TestCase):
    url = reverse('competition-list')

    def setUp(self) -> None:
        self.client = APIClient()
        self.title = 'qwe'

    def test_create_competition(self):
        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 0

        response = self.client.post(self.url, data={'title': self.title})
        competition_data = response.json()
        assert response.status_code == 201

        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 1

        response = self.client.get(f"{self.url}{competition_data['id']}/")
        data = response.json()
        assert data['title'] == self.title

    def test_delete_competition(self):
        response = self.client.post(self.url, data={'title': self.title})
        competition_id = response.json()['id']

        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 1

        self.client.delete(f"{self.url}{competition_id}/")
        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 0

    def test_update_competition(self):
        response = self.client.post(self.url, data={'title': self.title})
        competition_id = response.json()['id']

        response = self.client.get(f"{self.url}{competition_id}/")
        data = response.json()
        assert data['title'] == self.title

        new_title = 'asd'
        response = self.client.patch(f"{self.url}{competition_id}/", data={'title': new_title})
        data = response.json()
        assert data['title'] == new_title

        new_title = 'zxc'
        response = self.client.put(f"{self.url}{competition_id}/", data={'title': new_title})
        data = response.json()
        assert data['title'] == new_title
