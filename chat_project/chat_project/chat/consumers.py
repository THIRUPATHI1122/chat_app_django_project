import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.recipient_username = self.scope['url_route']['kwargs']['username']
        self.room_name = f"chat_{self.scope['user'].username}_{self.recipient_username}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender = self.scope['user']
        recipient = User.objects.get(username=self.recipient_username)
        content = data['message']

        # Save message to the database
        Message.objects.create(sender=sender, recipient=recipient, content=content)

        # Broadcast message
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': content,
                'sender': sender.username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
        }))
