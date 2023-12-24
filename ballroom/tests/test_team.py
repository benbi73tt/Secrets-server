from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework.test import APIClient

from ballroom.models import Trainer, TypeBallroomDancing, Team


def create_random_team():
    trainer = Trainer.objects.create(full_name=get_random_string(15))
    type_ballroom = TypeBallroomDancing.objects.create(program=get_random_string(3), title=get_random_string(5))
    return Team.objects.create(trainer=trainer, type=type_ballroom, founding_date=datetime.today().date())


class TeamTestCase(TestCase):
    url = reverse('team-list')

    def setUp(self) -> None:
        self.client = APIClient()
        self.trainer = Trainer.objects.create(full_name='Игорь Игорь Игорь')
        self.type_ballroom = TypeBallroomDancing.objects.create(program='СТС', title='Воронины')

    def test_create_team(self):
        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 0

        founding_date = datetime.today().date()
        response = self.client.post(self.url, data={'trainer': self.trainer.id, 'type': self.type_ballroom.id,
                                                    'founding_date': founding_date})
        team_data = response.json()
        assert response.status_code == 201

        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 1

        response = self.client.get(f"{self.url}{team_data['id']}/")
        data = response.json()
        assert data['trainer'] == self.trainer.id

    def test_delete_team(self):
        founding_date = datetime.today().date()
        response = self.client.post(self.url, data={'trainer': self.trainer.id, 'type': self.type_ballroom.id,
                                                    'founding_date': founding_date})
        team_id = response.json()['id']

        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 1

        self.client.delete(f"{self.url}{team_id}/")
        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 0

    def test_update_team(self):
        founding_date = datetime.today().date()
        response = self.client.post(self.url, data={'trainer': self.trainer.id, 'type': self.type_ballroom.id,
                                                    'founding_date': founding_date})
        team_id = response.json()['id']

        response = self.client.get(f"{self.url}{team_id}/")
        data = response.json()
        assert data['trainer'] == self.trainer.id

        new_trainer = Trainer.objects.create(full_name='Точно Игорь Игорь')
        response = self.client.patch(f"{self.url}{team_id}/", data={'trainer': new_trainer.id})
        data = response.json()
        assert data['trainer'] == new_trainer.id

        new_type_ballroom = TypeBallroomDancing.objects.create(program='СТС', title='Воронины')
        response = self.client.put(f"{self.url}{team_id}/", data={'type': new_type_ballroom.id})
        assert response.status_code == 400
        response = self.client.put(f"{self.url}{team_id}/",
                                   data={'trainer': new_trainer.id, 'type': new_type_ballroom.id,
                                         'founding_date': founding_date})
        data = response.json()
        assert data['trainer'] == new_trainer.id
        assert data['type'] == new_type_ballroom.id
