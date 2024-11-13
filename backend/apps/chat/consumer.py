import json

import redis
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.chat.service import create_chat
from apps.user.service import get_one_user_info
from utils.sensitive import filter_sensitive

redis_client = redis.StrictRedis(host='110.41.38.135', port=6379, db=0, decode_responses=True)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.user_id = None
            await self.accept()
            await self.channel_layer.group_add("chat_group", self.channel_name)
            print("WebSocket 连接已建立")
        except Exception as e:
            print(f"WebSocket 连接失败: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            if self.user_id:
                user = await self.safe_get_one_user_info({'id': self.user_id})
                if user:
                    await self.keep_latest_online_list("close", {"user_id": user.id, "nick_name": user.nick_name})
            await self.channel_layer.group_discard("chat_group", self.channel_name)
            print("WebSocket 连接已断开")
        except Exception as e:
            print(f"WebSocket 断开时发生错误: {str(e)}")

    async def receive(self, text_data):
        try:
            message = json.loads(text_data)
            message_type = message.get("type")

            if message_type == "init":
                await self.handle_init_message(message)

            elif message_type == "message":
                await self.handle_message(message)

            elif message_type == "revert":
                await self.handle_revert_message(message)

            elif message_type == "offline":
                await self.handle_offline_message(message)

        except Exception as e:
            print(f"接收消息时发生错误: {str(e)}")

    # 处理 "init" 消息类型
    async def handle_init_message(self, message):
        self.user_id = message.get("user_id")
        if self.user_id:
            user = await self.safe_get_one_user_info({'id': self.user_id})
            if user:
                message["nick_name"] = user.nick_name
                message["avatar"] = user.avatar
                await self.keep_latest_online_list("online", message)
        else:
            await self.send_online_to_all()

    # 处理 "message" 消息类型
    async def handle_message(self, message):
        message["content"] = await self.filter_sensitive(message["content"])
        user = await self.safe_get_one_user_info({"id": message["user_id"]})
        if user:
            message["nick_name"] = user.nick_name
            message["avatar"] = user.avatar
        res = await self.safe_create_chat(message)
        if res:
            message["id"] = res.id
        await self.send_to_all_clients(message)

    # 处理 "revert" 消息类型
    async def handle_revert_message(self, message):
        if message.get("message_id"):
            await self.send_to_all_clients(message)

    # 处理 "offline" 消息类型
    async def handle_offline_message(self, message):
        if message.get("user_id"):
            user = await self.safe_get_one_user_info({"id": message["user_id"]})
            if user:
                await self.keep_latest_online_list("close", {"user_id": user.id, "nick_name": user.nick_name})

    # 将在线用户信息存储到 Redis
    async def keep_latest_online_list(self, action, message):
        if action == "online":
            # 存储在线用户信息到 Redis
            redis_client.set(f"online:{message['user_id']}", json.dumps(message))
            print(f"{message['nick_name']} 上线了...")

        elif action == "close":
            # 移除离线用户
            redis_client.delete(f"online:{message['user_id']}")
            print(f"{message['nick_name']} 断开连接...")

        # 广播最新的在线用户列表
        await self.send_online_to_all()

    # 向所有客户端广播在线用户列表
    async def send_online_to_all(self):
        # 从 Redis 获取所有在线用户
        online_users = redis_client.keys("online:*")
        online_list = []
        for user_key in online_users:
            user_data = redis_client.get(user_key)
            if user_data:
                online_list.append(json.loads(user_data))

        message = json.dumps({
            "type": "onlineList",
            "list": online_list,
        })
        await self.channel_layer.group_send("chat_group", {"type": "chat_message", "message": message})

    # 向所有客户端广播消息
    async def send_to_all_clients(self, message):
        if isinstance(message, dict):
            message = await sync_to_async(dict)(message)
        message_json = json.dumps(message)
        await self.channel_layer.group_send("chat_group", {"type": "chat_message", "message": message_json})

    # 处理消息广播
    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=message)

    # 获取当前时间
    def now(self):
        import datetime
        return datetime.datetime.now()

    # 过滤敏感词
    async def filter_sensitive(self, content):
        return await database_sync_to_async(filter_sensitive)(content)

    # 获取用户信息
    async def safe_get_one_user_info(self, query_filters):
        return await database_sync_to_async(get_one_user_info)(query_filters)

    # 创建聊天记录
    async def safe_create_chat(self, message):
        return await database_sync_to_async(create_chat)(message)
