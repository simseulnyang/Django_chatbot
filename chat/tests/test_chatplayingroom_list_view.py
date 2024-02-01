import json

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from chat.models import ChatRolePlaying

User = get_user_model()

LOGIN_USER_URL = reverse("login")
CHATPLAYINGROOM_LIST_URL = reverse("chatroleplaying-list")


class ChatPlayingroomListViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # 테스트 사용자 생성
        cls.user1 = User.objects.create_user(email="testuser01@email.com", password="testpassword", name="testuser01")
        cls.user2 = User.objects.create_user(email="testuser02@email.com", password="testpassword", name="testuser02")

        cls.user1_data={
            "email": "testuser01@email.com",
            "password": "testpassword"
        }
        cls.user2_data={
            "email": "testuser02@email.com",
            "password": "testpassword"
        }

        # 테스트 chatplayingroom 생성
        cls.chatroom1 = ChatRolePlaying.objects.create(
            user=cls.user1,
            language="ko-kr",
            level="1",
            situation="빽다방에서 커피 주문하기",
            my_role="손님",
            gpt_role="빽다방 직원"
        )
        cls.chatroom2 = ChatRolePlaying.objects.create(
            user=cls.user1,
            language="ko-kr",
            level="1",
            situation="이디야에서 커피 주문하기",
            my_role="손님",
            gpt_role="이디야 직원"
        )
        cls.chatroom3 = ChatRolePlaying.objects.create(
            user=cls.user2,
            language="ko-kr",
            level="1",
            situation="스타벅스에서 커피 주문하기",
            my_role="손님",
            gpt_role="스타벅스 직원"
        )

    def setUp(self):
        res1 = self.client.post(LOGIN_USER_URL, data=json.dumps(self.user1_data), content_type="application/json",)
        self.access_token1 = res1.data["token"]["access"]

    def test_get_chatplayingroom_list_sucess(self):
        response = self.client.get(
            CHATPLAYINGROOM_LIST_URL,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token1}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_chatplayingroom_list_fail_unauthenticated(self):
        response = self.client.get(
            CHATPLAYINGROOM_LIST_URL,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)