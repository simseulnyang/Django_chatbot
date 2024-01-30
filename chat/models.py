from typing import List, Literal, TypedDict

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class GptMessage(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str


class Language(models.TextChoices):
    ENGLISH = "en-US", "English"
    KOREAN = "ko-kr", "Korean"


class Level(models.IntegerChoices):
    BEGINNER = 1, "초급"
    ADVENCED = 2, "고급"


class Conversation(models.Model):
    prompt = models.CharField(max_length=512)
    response = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)


class ChatRolePlaying(models.Model):
    class Meta:
        ordering = ["-pk"]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    conversations = models.ManyToManyField(
        Conversation, 
        verbose_name="대화내용")
    language = models.CharField(
        max_length=10, 
        choices=Language.choices, 
        default=Language.KOREAN, 
        verbose_name="대화 언어",
    )
    level = models.SmallIntegerField(
        choices=Level.choices, default=Level.BEGINNER, verbose_name="레벨"
    )
    situation = models.CharField(max_length=100, verbose_name="상황")
    situation_en = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="상황 (영문)",
        help_text="GPT 프롬프트에 직접적으로 활용됩니다. 비워두시면, situation 필드를 번역하여 자동 반영됩니다.",
    )
    my_role = models.CharField(max_length=100, verbose_name="내 역할")
    my_role_en = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="내 역할 (영문)",
        help_text="GPT 프롬프트에 직접적으로 활용됩니다. 비워두시면, my_role 필드를 번역하여 자동 반영됩니다.",
    )
    gpt_role = models.CharField(max_length=100, verbose_name="GPT 역할")
    gpt_role_en = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="GPT 역할 (영문)",
        help_text="GPT 프롬프트에 직접적으로 활용됩니다. 비워두시면, gpt_role 필드를 번역하여 자동 반영됩니다.",
    )

    def __str__(self):
        return f"{self.user.name}: {self.situation}"

    def get_initial_messages(self) -> List[GptMessage]:
        gpt_name = "RolePlayingBot"
        language = self.get_language_display()
        situation_en = self.situation_en
        my_role_en = self.my_role_en
        gpt_role_en = self.gpt_role_en

        if self.level == self.Level.BEGINNER:
            level_string = f"a beginner in {language}"
            level_word = "simple"
        elif self.level == self.Level.ADVANCED:
            level_string = f"a advanced learner in {language}"
            level_word = "advanced"
        else:
            raise ValueError(f"Invalid level : {self.level}")

        system_message = (
            f"You are helpful assistant supporting people learning {language}. "
            f"Your name is {gpt_name}. "
            f"Please assume that the user you are assisting is {level_string}. "
            f"And please write only the sentence without the character role."
        )

        user_message = (
            f"Let's have a conversation in {language}. "
            f"Please answer in {language} only "
            f"without providing a translation. "
            f"And please don't write down the pronunciation either. "
            f"Let us assume that the situation in '{situation_en}'. "
            f"I am {my_role_en}. The character I want you to act as is {gpt_role_en}. "
            f"Please make sure that I'm {level_string}, so please use {level_word} words "
            f"as much as possible. Now, start a conversation with the first sentence!"
        )

        return [
            GptMessage(role="system", content=system_message),
            GptMessage(role="user", content=user_message),
        ]