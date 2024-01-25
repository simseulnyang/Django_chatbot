from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

PROFILE_URL = reverse('profile')


def create_user(**params):
    """새로운 사용자 생성을 위한 Helper function"""
    return get_user_model().objects.create_user(**params)


class UserProfileAPITest(TestCase):
    def setUp(self):
        self.user = create_user(
            email="testuser1234@email.com",
            password="testpassword",
            name="testuser"
        )
        self.client - APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        res = self.client.post(PROFILE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            "email": self.user.email,
            "name": self.user.name,
        })

    def test_update_profile_success(self):
        payload = {'name': "newname", 'nickname': 'newnickname'}

        res = self.client.patch(PROFILE_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertEqual(self.user.profile.nickname, payload['nickname'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)