import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from channels.auth import login, AnonymousUser, get_user
from channels.db import database_sync_to_async
from .models import Product, ProductSerial

class ProductConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # if not self.scope["user"].is_anonymous:
        # await login(self.scope, user)
        self.user = await get_user(self.scope)
        if self.user.is_authenticated:
            # get current product name, throws if get fails
            self.product_name = self.scope['url_route']['kwargs']['product_name']
            self.product = await sync_to_async(Product.objects.get)(name=self.product_name)
            #check serial key, throws if get fails
            self.product_serial = await sync_to_async(ProductSerial.objects.get)(product=self.product, owner=self.user)
            #send disconnect signal for other instances of this product
            self.room_group_name = "product" + self.product_name + self.user.username
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'auth_message',
                    'message': 'disconnect'
                }
            )
            #join the room after others were disconnected
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
    async def auth_message(self, event):
        message = event['message']
        if(message == 'disconnect'):
            await self.disconnect(0)


    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass
