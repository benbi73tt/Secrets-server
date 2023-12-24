from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from ballroom.models import CompetitionProgram
from ballroom.tests.test_competition_program import create_random_competition
from ballroom.tests.test_member import create_random_member


class PointTestCase(TestCase):
    url = reverse('point-list')

    def setUp(self) -> None:
        self.client = APIClient()
        self.program = CompetitionProgram.objects.create(competition=create_random_competition())
        self.user = create_random_member()
        self.user_point = 5

    def test_create_point(self):
        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 0

        response = self.client.post(self.url, data={'user': self.user.id, 'program': self.program.id,
                                                    'user_point': self.user_point})
        point_data = response.json()
        assert response.status_code == 201

        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 1

        response = self.client.get(f"{self.url}{point_data['id']}/")
        data = response.json()
        assert data['user_point'] == self.user_point

    def test_delete_point(self):
        response = self.client.post(self.url, data={'user': self.user.id, 'program': self.program.id,
                                                    'user_point': self.user_point})
        point_id = response.json()['id']

        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 1

        self.client.delete(f"{self.url}{point_id}/")
        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 0

    def test_update_point(self):
        response = self.client.post(self.url, data={'user': self.user.id, 'program': self.program.id,
                                                    'user_point': self.user_point})
        point_id = response.json()['id']

        response = self.client.get(f"{self.url}{point_id}/")
        data = response.json()
        assert data['user_point'] == self.user_point

        new_user_point = 2
        response = self.client.patch(f"{self.url}{point_id}/", data={'user_point': new_user_point})
        data = response.json()
        assert data['user_point'] == new_user_point

        new_user = create_random_member()
        response = self.client.put(f"{self.url}{point_id}/", data={'user': new_user.id})
        assert response.status_code == 400
        response = self.client.put(f"{self.url}{point_id}/",
                                   data={'user': new_user.id, 'program': self.program.id,
                                         'user_point': new_user_point})
        data = response.json()
        assert data['user_point'] == new_user_point
        assert data['user'] == new_user.id
