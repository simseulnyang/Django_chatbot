from rest_framework import serializers
from .models import User as UserModel


class UserSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
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
