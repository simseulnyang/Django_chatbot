from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

LOGIN_USER_URL = reverse("login")


def create_user(**params):
    """새로운 사용자 생성을 위한 Helper function"""
    return User.objects.create_user(**params)


class UserLoginAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_post_login_success(self):
        create_user(
            email="testuser@email.com",
            password="testpassword",
            name="testuser",
            )
        payload = {
            "email" : "testuser@email.com",
            "password" : "testpassword",
        }
        res = self.client.post(LOGIN_USER_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_login_fail_invalid_password(self):
        create_user(
            email="testuser2@email.com",
            password="testpassword",
            name="testuser2",
            )
        payload = {
            "email" : "testuser2@email.com",
            "password" : "password",
        }
        res = self.client.post(LOGIN_USER_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_login_fail_invalid_email(self):
        create_user(
            email="testuser3@email.com",
            password="testpassword",
            name="testuser3",
            )
        payload = {
            "email" : "testuser3",
            "password" : "password",
        }
        res = self.client.post(LOGIN_USER_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)