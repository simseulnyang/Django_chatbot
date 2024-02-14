from django.shortcuts import get_list_or_404

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from chat.models import ChatRolePlaying as ChatRolePlayingModel
from chat.models import Conversation as ConversationModel
from chat.serializers import ChatRolePlayingSerializer, ChatRolePlayingCreateSerializer, ChatRolePlayingTranslateSerializer, ChatRolePlayingConversationSerializer

from dotenv import load_dotenv
import openai
import os

from django.http import JsonResponse


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


class ChatRolePlayingCreateAPIView(APIView):
    """
    'user', 'language', 'level', 'situation', 'my_role', 'gpt_role' 받아 새로운 RolePlaying Chatting Room을 생성합니다.

    Args:
        user(str) : user_id
        language(str) : Roleplaying 진행 시 사용할 언어
        level(str) : Roleplaying 진행 시 레벨
        situation(str) : Roleplaying 진행 시 상황
        my_role(str) : Roleplaying 진행 시 사용자의 역할
        gpt_role(str) : Roleplaying 진행 시 chatGPT의 역할
    
    Return:
        새로운 RolePlaying chatting Roome
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def post(self, request:Request) -> Response:
        serializer = ChatRolePlayingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
    

class ChatRolePlayingListAPIView(APIView):
    def get(self, request):
        chatlists = get_list_or_404(ChatRolePlayingModel, user=request.user)
        serializer = ChatRolePlayingSerializer(chatlists, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatplayingroomTranslatingAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def post(self, request):
        serializer = ChatRolePlayingTranslateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ChatRolePlayingDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        conversations = ConversationModel.objects.filter(chatplaying_id=request.chatplaying_id)
        serializer = ChatRolePlayingConversationSerializer(conversations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChatRolePlayingConversationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)