from rest_framework import serializers
from .models import User, Profile

class UserSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        password = user.password
        user.set_password(password)
        user.save()
        return user
    
    def update(self, *args, **kwargs):
        user = super().update(*args, **kwargs)
        password = user.password
        user.set_password(password)
        user.save()
        return user



class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['profile_img', 'about_me']


class UserSerializer(serializers.ModelSerializer):
    
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['email', 'nickname', 'date_joined', 'profile']