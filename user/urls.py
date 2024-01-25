from typing import List

from django.urls import URLPattern, path
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import SignupAPIView, LoginAPIView, LogoutAPIView, ProfileView


urlpatterns = [
    # user/
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]