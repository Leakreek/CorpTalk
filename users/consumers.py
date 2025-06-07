from channels.generic.websocket import AsyncWebsocketConsumer
import json

class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("status_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("status_updates", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            "status_updates",
            {
                "type": "send_status",
                "user": data["user"],
                "status": data["status"]
            }
        )

    async def send_status(self, event):
        await self.send(text_data=json.dumps({
            "user": event["user"],
            "status": event["status"]
        }))
