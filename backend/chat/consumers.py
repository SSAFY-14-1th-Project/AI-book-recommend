import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, ChatMessage
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user_id = data['user_id']

        room = ChatRoom.objects.get(id=self.room_id)
        user = User.objects.get(id=user_id)

        chat = ChatMessage.objects.create(
            room=room,
            sender=user,
            content=message
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': user.username,
                'created_at': chat.created_at.isoformat()
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
