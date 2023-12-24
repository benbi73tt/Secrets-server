from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient


class TypeBallroomDancingTestCase(TestCase):
    url = reverse('typeballroomdancing-list')

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_type_ballroom_dancing(self):
        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 0

        program = 'sts'
        title = 'voronini'
        response = self.client.post(self.url, data={'program': program, 'title': title})
        trainer_data = response.json()
        assert response.status_code == 201

        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 1

        response = self.client.get(f"{self.url}{trainer_data['id']}/")
        data = response.json()
        assert data['program'] == program

    def test_delete_type_ballroom_dancing(self):
        program = 'sts'
        title = 'voronini'
        response = self.client.post(self.url, data={'program': program, 'title': title})
        type_ballroom_dancing_id = response.json()['id']

        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 1

        self.client.delete(f"{self.url}{type_ballroom_dancing_id}/")
        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 0

    def test_update_type_ballroom_dancing(self):
        program = 'sts'
        title = 'voronini'
        response = self.client.post(self.url, data={'program': program, 'title': title})
        type_ballroom_dancing_id = response.json()['id']

        response = self.client.get(f"{self.url}{type_ballroom_dancing_id}/")
        data = response.json()
        assert data['program'] == program

        new_program = 'tnt'
        response = self.client.patch(f"{self.url}{type_ballroom_dancing_id}/", data={'program': new_program})
        data = response.json()
        assert data['program'] == new_program
        assert data['title'] == title

        new_program = '5'
        new_title = 'Следствие'
        response = self.client.put(f"{self.url}{type_ballroom_dancing_id}/", data={'program': new_program})
        assert response.status_code == 400
        response = self.client.put(f"{self.url}{type_ballroom_dancing_id}/",
                                   data={'program': new_program, 'title': new_title})
        data = response.json()
        assert data['program'] == new_program
        assert data['title'] == new_title
