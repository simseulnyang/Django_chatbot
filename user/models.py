from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):

    def _create_user(self, email, nickname, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('User must have an email')

        now = timezone.localtime()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            nickname=nickname,
            password=password,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=True,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # create_user
    def create_user(self, email, password, **extra_fields):

        nickname = extra_fields.get('nickname', '사용자')

        return self._create_user(email, nickname, password, False, False, **extra_fields)

    # create_superuser
    def create_superuser(self, email, password, **extra_fields):

        nickname = extra_fields.get('nickname', '관리자')

        return self._create_user(email, nickname, password, True, True, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField("이메일주소", unique=True, max_length=255)
    nickname = models.CharField("닉네임", max_length=10, null=True, blank=True)
    is_staff = models.BooleanField("관리자권한", default=False)
    is_superuser = models.BooleanField("관리자", default=False)
    is_active = models.BooleanField("계정활성화", default=True)
    last_login = models.DateTimeField("마지막 로그인 시간", null=True, blank=True)
    date_joined = models.DateTimeField("가입일", auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email} / {self.nickname}"


class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    profile_img = models.ImageField(null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_nickname(self):
        return self.user.nickname
    
    def __str__(self):
        return f"{self.user.nickname} / {self.user}"
