from rest_framework import serializers
from rest_framework.serializers import PrimaryKeyRelatedField

from chat.translators import google_translate
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


class ChatRolePlayingTranslateSerializer(serializers.ModelSerializer):
    situation_en = serializers.SerializerMethodField()
    my_role_en = serializers.SerializerMethodField()
    gpt_role_en = serializers.SerializerMethodField()

    class Meta:
        model = ChatRolePlaying
        fields = [
            "language",
            "level",
            "situation",
            "situation_en",
            "my_role",
            "my_role_en",
            "gpt_role",
            "gpt_role_en",
        ]

    def get_situation_en(self, obj):
        if obj.situation_en:
            return obj.situation_en
        if obj.situation:
            return self._translate(obj.situation)
        return None

    def get_my_role_en(self, obj):
        if obj.my_role_en:
            return obj.my_role_en
        if obj.my_role:
            return self._translate(obj.my_role)
        return None

    def get_gpt_role_en(self, obj):
        if obj.gpt_role_en:
            return obj.gpt_role_en
        if obj.gpt_role:
            return self._translate(obj.gpt_role)
        return None

    @staticmethod
    def _translate(origin_text: str) -> str:
        translated = google_translate(origin_text, "auto", "en")
        if not translated:
            raise serializers.ValidationError("구글 번역을 할 수 없습니다.")
        return translated