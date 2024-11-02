# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import RequestTemplate

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the user from the session if needed
        self.user = self.scope['user']
        
        # Define a group name based on user or department
        self.group_name = f"user_{self.user.id}" if self.user.is_authenticated else "anonymous_group"

        # Add this channel to the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Remove the channel from the group when the connection is closed
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive a message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')

        # Example of echoing back the message (not required, just for testing)
        await self.send(text_data=json.dumps({
            'message': message
        }))

    # Method to send notification messages
    async def send_notification(self, event):
        # Send the notification data to the WebSocket client
        await self.send(text_data=json.dumps({
            'notification': event['notification']
        }))
