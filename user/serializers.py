from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name']


class UserSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'name', 'password']
        extra_kwargs = {"password": {"write_only": True, "required": True, "min_length": 5}}

    def validate(self, data):
        email = data.get('email', '')
        password = data.get('password', '')

        email_id = email.split('@')[0]
        if email_id in password or password in email_id:
            raise ValidationError("비밀번호와 이메일의 id 부분이 유사합니다. 다른 비밀번호를 선택하세요.")
        
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            name=validated_data["name"],
            password=validated_data["password"]
        )
        return user
    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        
        if user is None:
            raise serializers.ValidationError("email or Password is Incorrect!")
        
        return data
    
    def get_token(self, user):
        if user is not None:
            refresh = TokenObtainPairSerializer.get_token(user)
            refresh["email"] = user.email
            data = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            return data
        return None
    
    def create(self, validated_data):
        user = authenticate(email=validated_data["email"], password=validated_data["password"])
        
        if user is not None:
            user.is_active = True
            user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['profile_img', 'about_me']


