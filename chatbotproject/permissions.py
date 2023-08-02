from rest_framework.permissions import BasePermission
from datetime import timedelta, datetime
from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework import status


class IsAdminOrIsAuthenticatedReadOnly(BasePermission):
    """
    admin 사용자는 모두 가능, 로그인 사용자는 조회만 가능
    """
    