from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Django channels & chatGPT를 통한 채팅서비스",
        default_version='v2',
        description="simseulnyang의 개인프로젝트",
        contact=openapi.Contact(email="happysseul627@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('chat/', include('chat.urls')),
    # Swagger
    path("swagger/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
