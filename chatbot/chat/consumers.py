import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    """
    Handles WebSocket connections for chat rooms.
    """
    async def connect(self):
        """
        Called when a WebSocket connection is established.
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """
        Called when a WebSocket connection is closed.
        """
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Called when a message is received from the WebSocket.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = self.scope['user'].id  # Get the user ID from the scope

        # Get the user object and room object
        user = await self.get_user_object(user_id)
        room = await self.get_room_object(self.room_name)

        # Save the message to the database
        await self.save_message(room, user, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user.username,  # Send the username
                'user_id': user.id,
                'timestamp': str(self.get_current_time())
            }
        )

    async def chat_message(self, event):
        """
        Called when a message is sent to the room group.
        """
        message = event['message']
        user = event['user']
        user_id = event['user_id']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'user_id': user_id,
            'timestamp': timestamp
        }))

    @database_sync_to_async
    def get_user_object(self, user_id):
        """
        Retrieves a user object from the database.
        """
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def get_room_object(self, room_name):
        """
        Retrieves a room object from the database.
        """
        return Room.objects.get(name=room_name)

    @database_sync_to_async
    def save_message(self, room, user, message):
        """
        Saves a message to the database.
        """
        Message.objects.create(room=room, user=user, text=message)

    @database_sync_to_async
    def get_current_time(self):
        from django.utils import timezone
        return timezone.now()