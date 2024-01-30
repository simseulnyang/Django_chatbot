from rest_framework import serializers
from chat.models import ChatRolePlaying, Conversation

class ChatRolePlayingCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatRolePlaying
        fields = ['user', 'language', 'level', 'situation', 'my_role', 'gpt_role']


class ChatRolePlayingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatRolePlaying
        fields = '__all__'


class ChatRolePlayingConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['prompt', 'response']