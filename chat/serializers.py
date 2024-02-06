from rest_framework import serializers
from rest_framework.serializers import PrimaryKeyRelatedField

from chat.models import ChatRolePlaying, Conversation
from user.models import User

class ChatRolePlayingCreateSerializer(serializers.ModelSerializer):
    user= PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ChatRolePlaying
        fields = ['user', 'language', 'level', 'situation', 'my_role', 'gpt_role']

    def create(self, validated_data):
        chatplayingroom = super().create(validated_data)
        return chatplayingroom


class ChatRolePlayingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatRolePlaying
        fields = '__all__'


class ChatRolePlayingConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['prompt', 'response']