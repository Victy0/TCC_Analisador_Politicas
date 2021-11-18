import json
from random import randint
from time import sleep

from channels.generic.websocket import AsyncWebsocketConsumer

class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        await self.accept()
        
        print("conectado")
        
        await self.send(text_data=json.dumps({
            'message': 'message'
        }))

    async def disconnect(self, close_code):
        print("desconectado")

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': 'message'
        }))