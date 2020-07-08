import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.auth import login, AnonymousUser, get_user
from channels.db import database_sync_to_async


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         self.send(text_data=json.dumps({
#             'message': message
#         }))


class ProductConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # if not self.scope["user"].is_anonymous:
        # await login(self.scope, user)
        self.user = await get_user(self.scope)
        if self.user.is_authenticated:
            self.product_name = self.scope['url_route']['kwargs']['product_name']
            if self.product_name == "dentslicer":
                await self.accept()
            
    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass
        # text_data_json = json.loads(text_data)