import json

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


CREATE_USER_URL = reverse("signup")


def create_user(**params):
    """새로운 사용자 생성을 위한 Helper function"""
    return User.objects.create_user(**params)


class UserSignupAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        payload = {
            "email": "testuser@example.com",
            "password": "testpassword",
            "name": "testname",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        print(res)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["email"], "testuser@example.com")
        self.assertNotIn("password", res.data)

    def test_user_exists(self):
        payload = {
            "email": "admin@email.com",
            "password": "admin1234!",
            "name": "testname",
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        payload = {
            "email": "testuser1@example.com",
            "password": "pass",
            "name": "testname",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = User.objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_password_similarity_validator(self):
        payload = {
            "email": "testuser2@example.com",
            "password": "testuser",
            "name": "testname",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = User.objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)