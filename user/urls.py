from django.urls import path, include
from django.contrib import admin
from user import views
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenObtainPairView,
)

urlpatterns = [
    # user/
    path('', views.UserView.as_view()),
    path('api/token/', views.UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]