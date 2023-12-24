from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework.test import APIClient

from ballroom.models import Competition


def create_random_competition():
    return Competition.objects.create(title=get_random_string(7))


class CompetitionProgramTestCase(TestCase):
    url = reverse('competitionprogram-list')

    def setUp(self) -> None:
        self.client = APIClient()
        self.competition = create_random_competition()

    def test_create_competition_program(self):
        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 0

        response = self.client.post(self.url, data={'competition': self.competition.id})
        competition_program_data = response.json()
        assert response.status_code == 201

        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 1

        response = self.client.get(f"{self.url}{competition_program_data['id']}/")
        data = response.json()
        assert data['competition'] == self.competition.id

    def test_delete_competition_program(self):
        response = self.client.post(self.url, data={'competition': self.competition.id})
        competition_program_id = response.json()['id']

        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 1

        self.client.delete(f"{self.url}{competition_program_id}/")
        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 0

    def test_update_competition_program(self):
        response = self.client.post(self.url, data={'competition': self.competition.id})
        competition_program_id = response.json()['id']

        response = self.client.get(f"{self.url}{competition_program_id}/")
        data = response.json()
        assert data['competition'] == self.competition.id

        new_competition = create_random_competition()
        response = self.client.patch(f"{self.url}{competition_program_id}/", data={'competition': new_competition.id})
        data = response.json()
        assert data['competition'] == new_competition.id

        new_competition = create_random_competition()
        response = self.client.put(f"{self.url}{competition_program_id}/", data={'competition': new_competition.id})
        data = response.json()
        assert data['competition'] == new_competition.id
