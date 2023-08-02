from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from user.jwt_claim_serializer import UserTokenObtainPairSerializer

from django.shortcuts import render
from .models import User as UserModel

from user.serializers import UserSignupSerializer, ProfileSerializer, UserSerializer


# TokenObtainPairView : urls.py에서 import했고, 토큰을 발급받기 위해 사용
class SeasonTokenObtainPairView(TokenObtainPairView):
    # serializer_class에 커스터마이징된 시리얼라이저를 넣어 준다.
    serializer_class = UserTokenObtainPairSerializer


class UserView(APIView):

    # 사용자 정보 조회
    def get(self, request):
        data = UserModel.objects.get(id=request.user.id)
        return Response(UserSignupSerializer(data).data, status=status.HTTP_200_OK)
    
    # 회원가입
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '회원가입이 완료되었습니다!'})
        else:
            return Response({'message': f'${serializer.errors}'}, 400)


    # 회원 정보 수정
    def put(self, request):
        user = UserModel.objects.get(id=request.user.id)
        serializer = UserSignupSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 회원 탈퇴
    def delete(self, request):
        user = UserModel.objects.get(id=request.user.id)
        if user:
            user.is_active = False
            return Response({"message": "회원탈퇴 성공"}, status=status.HTTP_200_OK)
        return Response({"message": "회원탈퇴 실패"}, status=status.HTTP_400_BAD_REQUEST)
    


# 인가된 사용자만 접근할 수 있는 View 생성
class OnlyAuthenticatedUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
		
    # JWT 인증방식 클래스 지정하기
    authentication_classes = [JWTAuthentication]

    def get(self, request):
		# Token에서 인증된 user만 가져온다.
        user = request.user
        print(f"user 정보 : {user}")
        if not user:
            return Response({"error": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": "Accepted"})
    


class ProfileView(APIView):

    def get(self, request, pk):
        user = UserModel.objects.get(pk=pk)
        serializer = ProfileSerializer(user, data=request.data)
        serializer.save()
        return Response(serializer, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        user = UserModel.objects.get(pk=pk)
        serializer = ProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)