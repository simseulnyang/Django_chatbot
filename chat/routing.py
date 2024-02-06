from django.urls import path
from chat.consumers import ChatRolePlayingConsumer

websocket_urlpatterns = [
    path("ws/chat/<int:room_pk>/", ChatRolePlayingConsumer.as_asgi()),
]