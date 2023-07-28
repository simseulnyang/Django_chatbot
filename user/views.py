from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from user.serializers import UserSignupSerializer
from user.jwt_claim_serializer import UserTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserView(APIView):

    # 사용자 정보 조회
    def get(self, request):
        return Response(UserSignupSerializer(request.user).data, status=status.HTTP_200_OK)
    
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
        return Response({'message': 'put method!'})
    
    def delete(self, request):
        return Response({'message': 'delete method!'})
    



class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer