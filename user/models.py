from django.contrib.auth.models import AbstractUser
from django.db import models

from user.manager import UserManager


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=10)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField( default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "user"

    def __str__(self):
        return f"{self.email} / {self.name}"


class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=128)
    profile_img = models.ImageField(null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nickname} / {self.user}"
    
    def get_nickname(self) -> str:
        if self.nickname is None:
            return Profile("nickname", f"사용자{self.user.pk}")