from django.contrib.auth import logout
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User
from user.serializers import UserSerializer, UserSignupSerializer, UserLoginSerializer, ProfileSerializer


class SignupAPIView(APIView):
    permission_classes=[permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="유저 회원가입",
        request_body=UserSignupSerializer,
        responses={status.HTTP_201_CREATED: UserSerializer},
    )

    def post(self, request: Request) -> Response:
        """
        이메일(email)과 비밀번호(password), 사용자 이름(name)을 받아 새로운 사용자 계정을 생성합니다.

        Args:
            email (str): 사용자 이메일
            password (str): 사용자 계정 비밀번호
            name (str): 사용자 이름
        
        Return:
            User: 생성된 사용자 객체
        """
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="유저 로그인",
        request_body=UserLoginSerializer,
        responses={status.HTTP_200_OK: UserSerializer},
    )

    def post(self, request: Request) -> Response:
        """
        이메일(email)과 비밀번호(password)를 받아 유저 계정을 활성화하고 JWT 토큰을 발급합니다.

        Args:
            email(str) : 사용자 계정 이메일
            password(str) : 사용자 계정 비밀번호

        Retur:
            token: access token과 refresh token 발급
        """
        serializer=UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="유저 로그아웃",
        responses={status.HTTP_202_ACCEPTED},
    )

    def post(self, request:Request) -> Response:
        user = request.user
        refresh_token = RefreshToken.for_user(user)
        refresh_token.blacklist()
        logout(request)
        return Response({"message":"로그아웃 성공"},status=status.HTTP_200_OK)



class ProfileView(APIView):

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = ProfileSerializer(user, data=request.data)
        serializer.save()
        return Response(serializer, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = ProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)