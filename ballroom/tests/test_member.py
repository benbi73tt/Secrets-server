from io import BytesIO

from PIL import Image
from django.core.files.base import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework.test import APIClient

from ballroom.models import Member
from ballroom.tests.test_team import create_random_team


def create_random_member():
    return Member.objects.create(
        lastname=get_random_string(15),
        team=create_random_team(),
        image=get_image_file(),
        city=get_random_string(10),
        level=get_random_string(2)
    )


def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
    file_obj = BytesIO()
    image = Image.new("RGB", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return File(file_obj, name=name)


class MemberTestCase(TestCase):
    url = reverse('member-list')

    def setUp(self) -> None:
        self.client = APIClient()
        self.image = get_image_file()
        self.team = create_random_team()
        self.lastname = 'Игорь'
        self.city = 'Ульяновск'
        self.level = 'SSS'

    def test_create_member(self):
        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 0

        response = self.client.post(self.url, data={
            'lastname': self.lastname,
            'team': self.team.id,
            'image': self.image,
            'city': self.city,
            'level': self.level,
        })
        member_data = response.json()
        assert response.status_code == 201

        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 1

        response = self.client.get(f"{self.url}{member_data['id']}/")
        data = response.json()
        assert data['lastname'] == self.lastname

    def test_delete_member(self):
        response = self.client.post(self.url, data={
            'lastname': self.lastname,
            'team': self.team.id,
            'image': self.image,
            'city': self.city,
            'level': self.level,
        })
        member_id = response.json()['id']

        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 1

        self.client.delete(f"{self.url}{member_id}/")
        response = self.client.get(self.url)
        data = response.json()
        assert data['count'] == 0

    def test_update_member(self):
        response = self.client.post(self.url, data={
            'lastname': self.lastname,
            'team': self.team.id,
            'image': self.image,
            'city': self.city,
            'level': self.level,
        })
        member_id = response.json()['id']

        response = self.client.get(f"{self.url}{member_id}/")
        data = response.json()
        assert data['lastname'] == self.lastname

        new_city = 'Москва'
        new_level = 'A'
        response = self.client.patch(f"{self.url}{member_id}/", data={'city': new_city,
                                                                      'level': new_level})
        data = response.json()
        assert data['city'] == new_city
        assert data['level'] == new_level

        new_lastname = 'Точно'
        response = self.client.put(f"{self.url}{member_id}/", data={'lastname': new_lastname})
        assert response.status_code == 400

        response = self.client.put(f"{self.url}{member_id}/", data={
            'lastname': new_lastname,
            'team': self.team.id,
            'image': get_image_file(),
            'city': new_city,
            'level': new_level,
        })
        data = response.json()
        assert data['city'] == new_city
        assert data['level'] == new_level
        assert data['lastname'] == new_lastname
