from typing import List
from channels.generic.websocket import JsonWebsocketConsumer

from chat.models import ChatRolePlaying, GptMessage
from user.models import User

import openai


class ChatRolePlayingConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gpt_messages: List[GptMessage] = []

    def connect(self):
        room = self.get_room()
        if room is None:
            self.close()
        else:
            self.accept()

            self.gpt_messages = room.get_initial_messages()

            assistant_message = self.get_query()
            self.send_json({
                "type": "assistant-message",
                "message": assistant_message,
            })

    def receive_json(self, content, **kwargs):
        if content["type"] == "user-message":
            assistant_message = self.get_query(user_query=content["message"])
            self.send_json(
                {
                    "type": "assistant-message",
                    "message": assistant_message,
                }
            )
        else:
            self.send_json({
                "type": "error",
                "message": f"Invalid type: {content['type']}",
            })

    def get_room(self) -> ChatRolePlaying | None:
        user: User = self.scope["user"]
        room_pk = self.scope["url_route"]["kwargs"]["room_pk"]
        room : ChatRolePlaying = None

        if user.is_authenticated:
            try:
                room = ChatRolePlaying.objects.get(pk=room_pk, user=user)
            except ChatRolePlaying.DoesNotExist:
                pass

        return room
    
    def get_query(self, command_query:str = None, user_query:str = None) -> str :
        if command_query is not None and user_query is not None:
            raise ValueError("command_query 인자와 user_query 인자는 동시에 사용할 수 없습니다.")
        elif command_query is not None:
            self.gpt_messages.append(GptMessage(role="user", content=command_query))
        elif user_query is not None:
            self.gpt_messages.append(GptMessage(role="user", content=user_query))

        response_dict = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.gpt_messages,
            temperature=1
        )
        response_role = response_dict["choices"][0]["message"]["role"]
        response_content = response_dict["choices"][0]["message"]["content"]

        if command_query is None:
            gpt_message = GptMessage(role=response_role, content=response_content)
            self.gpt_messages.append(gpt_message)

        return response_content