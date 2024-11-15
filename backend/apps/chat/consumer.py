import json

import redis
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from utils.result import result, throw_error, ERRORCODE
from apps.chat.service import create_chat, delete_chats, delete_one_chat, get_chat_list, get_one_chat, get_all_chats
from apps.user.service import get_one_user_info
from utils.sensitive import filter_sensitive
from utils.minioUpload import delete_minio_imgs

redis_client = redis.StrictRedis(host='110.41.38.135', port=6379, db=0, decode_responses=True)

chat_error_code = ERRORCODE['CHAT']
auth_error_code = ERRORCODE['AUTH']


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

            elif message_type == "offline":
                await self.handle_offline_message(message)

            elif message_type == "getChatList":
                await self.handle_getChatList_message(message)

            elif message_type == "message":
                await self.handle_message(message)

            elif message_type == "revert":
                await self.handle_revert_message(message)

            elif message_type == "clearHistory":
                await self.handle_clearHistory_message(message)

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

    # 处理 "offline" 消息类型
    async def handle_offline_message(self, message):
        if message.get("user_id"):
            user = await self.safe_get_one_user_info({"id": message["user_id"]})
            if user:
                await self.keep_latest_online_list("close", {"user_id": user.id, "nick_name": user.nick_name})

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
        response = result("消息发送成功", message)
        response["type"] = "message"
        await self.send_to_all_clients(response)

    # 处理 "revert" 消息类型
    async def handle_revert_message(self, message):
        try:
            chat_id = message.get("message_id")
            user_id = message.get("user_id")
            if chat_id:
                one = await self.get_one_chat(chat_id)
                if not one:
                    response = throw_error(chat_error_code, "消息不存在")
                    response["type"] = "revert"
                    await self.send_to_all_clients(response)
                    return

                if one.user_id == user_id:
                    if one.content_type == "image":
                        content = one.content
                        arr = [content.split("/").pop()]
                        await sync_to_async(delete_minio_imgs)(arr)

                    await self.delete_one_chat(chat_id, user_id)
                    response = result("撤回成功", {"message_id": chat_id})
                    response["type"] = "revert"
                    await self.send_to_all_clients(response)
                else:
                    response = throw_error(chat_error_code, "撤回失败，不允许撤回他人消息")
                    response["type"] = "revert"
                    await self.send_to_all_clients(response)
        except Exception as err:
            print(f"撤回消息时发生错误: {str(err)}")
            response = throw_error(chat_error_code, "撤回失败")
            response["type"] = "revert"
            await self.send_to_all_clients(response)

    async def handle_clearHistory_message(self, message):
        try:
            user_info = await self.safe_get_one_user_info({id: message["user_id"]})
            if user_info.role == 1:
                arr = await self.get_all_chats()
                if arr:
                    arr = [item.content.split("/").pop() for item in arr]
                    await sync_to_async(delete_minio_imgs)(arr)

                await self.delete_chats()

                response = result("聊天记录已清空", {})
                response["type"] = "clearHistory"
                await self.send_to_all_clients(response)
            else:
                response = throw_error(auth_error_code, "权限不足，无法清空聊天记录")
                response["type"] = "clearHistory"
                await self.send_to_all_clients(response)
        except Exception as err:
            print(f"清空聊天记录时发生错误: {str(err)}")
            response = throw_error(chat_error_code, "清空聊天记录失败")
            response["type"] = "clearHistory"
            await self.send_to_all_clients(response)

    async def handle_getChatList_message(self, message):
        chat_list = await self.get_chat_list(message)

        response = result("获取聊天列表成功", {
            "list": chat_list.get("list", []),
            "total": chat_list.get("total", 0),
        })
        response["type"] = "getChatList"
        await self.send_to_all_clients(response)

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

    async def get_chat_list(self, params):
        return await database_sync_to_async(get_chat_list)(params)

    async def get_all_chats(self):
        return await database_sync_to_async(get_all_chats)()

    async def clear_all_chats(self):
        return await database_sync_to_async(delete_chats)()

    async def get_one_chat(self, chat_id):
        return await database_sync_to_async(get_one_chat)(chat_id)

    async def delete_chats(self):
        return await database_sync_to_async(delete_chats)()

    async def delete_one_chat(self, chat_id, user_id):
        return await database_sync_to_async(delete_one_chat)(chat_id, user_id)
