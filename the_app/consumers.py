import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User

from .models import Chatroom, ChatroomMessages

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.chatroom = self.scope['url_route']['kwargs']['chatroom']
        self.room_group_name = f"chat_{self.chatroom}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # I wrote this code
    @sync_to_async
    def get_chat_history(self):
        return ChatroomMessages.objects.filter(chatroom__chatroom=self.chatroom).order_by('timestamp')

    async def send_chat_history(self):
        chat_history = await self.get_chat_history()
        for message in chat_history:
            await self.send(text_data=json.dumps({
                'type': 'chat.message',
                'user': message.user.username,
                'message': message.message,
            }))

    @sync_to_async
    def save_chat_message(self, user, chatroom, message):
        return ChatroomMessages.objects.create(user=user, chatroom=chatroom, message=message)

    async def receive(self, text_data):
        user = self.scope["user"]
        message = text_data

        # extract the message content without additional processing
        message_content = message.strip().split(': ', 1)[1]  # Split and take the part after the first ": "
        # remove the trailing "}" from message_content if it exists
        message_content = message_content.rstrip('"}')

        chatroom = await sync_to_async(Chatroom.objects.get)(chatroom=self.chatroom)

        try:
            # Create and save the chat message (wrapped in sync_to_async)
            await self.save_chat_message(user, chatroom, message_content)

            # Send the message to the room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    'user': user.username,
                    'message': message_content,
                }
            )
        except Exception as e:
            # Handle exceptions, log them, or send an error message to the client
            error_message = {"error": str(e)}
            await self.send(text_data=json.dumps(error_message))
    # end of code I wrote
    
    async def chat_message(self, event):
        user = event['user']
        message = event['message']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat.message',
            'user': user,
            'message': user + ": " + message,
        }))
