import json

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

User = get_user_model()

LOGIN_USER_URL = reverse("login")
CHATPLAYINGROOM_TRANSLATION_URL = reverse("chatplayingTranslation")


class ChatPlayingroomTranslationViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # 테스트 사용자 생성
        cls.user1 = User.objects.create_user(email="testuser01@email.com", password="testpassword", name="testuser01")

        cls.user1_data={
            "email": "testuser01@email.com",
            "password": "testpassword"
        }

    def setUp(self):
        res1 = self.client.post(LOGIN_USER_URL, data=json.dumps(self.user1_data), content_type="application/json",)
        self.access_token1 = res1.data["token"]["access"]

    def test_post_chatplayingroom_translation_sucess(self):
        payload = {
            "user": 1,
            "language": "ko-kr",
            "level": "1",
            "situation": "빽다방에서 커피 주문하기3",
            "my_role": "손님",
            "gpt_role": "빽다방 직원",
        }
        response = self.client.post(
            CHATPLAYINGROOM_TRANSLATION_URL,
            payload,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token1}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('situation_en', response.data)

    def test_post_chatplayingroom_translation_fail_unauthenticated(self):
        payload = {
            "user": 2,
            "language": "ko-kr",
            "level": "1",
            "situation": "빽다방에서 커피 주문하기3",
            "my_role": "손님",
            "gpt_role": "빽다방 직원",
        }
        response = self.client.post(
            CHATPLAYINGROOM_TRANSLATION_URL,
            payload
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_chatplayingroom_translation_fail_not_enough_params(self):
        payload = {
            "user": 1,
            "language": "ko-kr",
            "level": "1",
            "situation": "빽다방에서 커피 주문하기3",
            "gpt_role": "빽다방 직원",
        }
        response = self.client.post(
            CHATPLAYINGROOM_TRANSLATION_URL,
            payload,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token1}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)