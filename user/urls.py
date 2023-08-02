from django.urls import path, include
from django.contrib import admin
from user import views
from user.views import SeasonTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # user/
    path('', views.UserView.as_view()),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('api/authonly/', views.OnlyAuthenticatedUserView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/season/token/', SeasonTokenObtainPairView.as_view(), name='season_token'),
]