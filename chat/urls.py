from django.urls import path

from chat.views import ChatRolePlayingCreateAPIView, ChatRolePlayingListAPIView


urlpatterns = [
	path("", ChatRolePlayingListAPIView.as_view(), name="chatroleplaying-list"),
    path("new/", ChatRolePlayingCreateAPIView.as_view(), name="chatroleplaying-create"),
]
