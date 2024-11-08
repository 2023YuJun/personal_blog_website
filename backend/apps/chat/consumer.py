import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import connection
from channels.db import database_sync_to_async
from apps.chat.service import create_chat
from apps.user.service import get_one_user_info
from utils.sensitive import filter_sensitive

online_list = []


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = None
        await self.accept()
        await self.channel_layer.group_add("chat_group", self.channel_name)
        print("WebSocket 连接已建立并加入 chat_group.")

    async def disconnect(self, close_code):
        if self.user_id:
            user = await self.safe_get_one_user_info({'id': self.user_id})
            if user:
                await self.keep_latest_online_list("close", {"user_id": user.id, "nick_name": user.nick_name})
        await self.channel_layer.group_discard("chat_group", self.channel_name)
        print("WebSocket 连接已断开并离开 chat_group.")

    async def receive(self, text_data):
        message = json.loads(text_data)
        message_type = message.get("type")

        if message_type == "init":
            self.user_id = message.get("user_id")
            if self.user_id:
                user = await self.safe_get_one_user_info({'id': self.user_id})
                if user:
                    message["nick_name"] = user.nick_name
                    message["avatar"] = user.avatar

                    await self.keep_latest_online_list("online", message)
            else:
                await self.send_online_to_all()

        elif message_type == "message":
            message["content"] = await self.filter_sensitive(message["content"])
            user = await self.safe_get_one_user_info({"id": message["user_id"]})
            if user:
                message["nick_name"] = user.nick_name
                message["avatar"] = user.avatar
            res = await self.safe_create_chat(message)
            if res:
                message["id"] = res.id
            await self.send_to_all_clients(message)

        elif message_type == "revert":
            if message.get("message_id"):
                await self.send_to_all_clients(message)

        elif message_type == "offline":
            if message.get("user_id"):
                user = await self.safe_get_one_user_info({"id": message["user_id"]})
                if user:
                    await self.keep_latest_online_list("close", {"user_id": user.id, "nick_name": user.nick_name})

    async def keep_latest_online_list(self, action, message):
        global online_list
        index = next((i for i, item in enumerate(online_list) if item['user_id'] == message['user_id']), None)

        if action == "online":
            if index is not None:
                online_list.pop(index)
            online_list.append({
                "user_id": message['user_id'],
                "nick_name": message['nick_name'],
                "avatar": message['avatar'],
                "createTime": self.now().isoformat(),
            })
            print(f"{message['nick_name']} 上线了...")

        elif action == "close":
            if index is not None:
                online_list.pop(index)
                if message.get('nick_name'):
                    print(f"{message['nick_name']} 断开连接...")

        await self.send_online_to_all()

    async def send_online_to_all(self):
        message = json.dumps({
            "type": "onlineList",
            "list": online_list,
        })
        await self.channel_layer.group_send("chat_group", {"type": "chat_message", "message": message})

    async def send_to_all_clients(self, message):
        if isinstance(message, dict):
            message = await sync_to_async(dict)(message)
        message_json = json.dumps(message)
        await self.channel_layer.group_send("chat_group", {"type": "chat_message", "message": message_json})


    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=message)

    def now(self):
        import datetime
        return datetime.datetime.now()

    async def filter_sensitive(self, content):
        return await database_sync_to_async(filter_sensitive)(content)

    async def safe_get_one_user_info(self, query_filters):
        return await database_sync_to_async(get_one_user_info)(query_filters)

    async def safe_create_chat(self, message):
        return await database_sync_to_async(create_chat)(message)
