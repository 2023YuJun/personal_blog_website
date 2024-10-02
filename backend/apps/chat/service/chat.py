from django.utils.functional import Promise

from ..models import Chat
from ...user.service.user import user_service
from django.db.models import Q


class ChatService:
    """
    聊天服务层
    """

    async def create_chat(self, chat):
        """
        新增聊天
        """
        chat_obj = await Chat.objects.create(
            content_type=chat.get('content_type'),
            content=chat.get('content'),
            user_id=chat.get('user_id')
        )
        return chat_obj

    async def delete_chats(self):
        """
        删除所有聊天记录
        """
        res = await Chat.objects.all().delete()
        return res

    async def delete_one_chat(self, chat_id):
        """
        删除单条聊天记录（撤销聊天）
        """
        res = await Chat.objects.filter(id=chat_id).delete()
        return res

    async def get_one_chat(self, chat_id):
        """
        根据id获取聊天信息
        """
        res = await Chat.objects.filter(id=chat_id).first()
        return res if res else None

    async def get_all_chats(self):
        """
        获取所有的聊天记录
        """
        res = await Chat.objects.filter(content_type="image").values("content")
        return list(res)

    async def get_chat_list(self, params):
        """
        分页获取聊天列表
        """
        size = params.get('size', 10)
        last_id = params.get('last_id')

        where_opt = Q()
        current = None

        if last_id:
            where_opt &= Q(id__lt=last_id)
            current = last_id
        else:
            last_chat = await Chat.objects.order_by("-id").first()
            if last_chat:
                current = last_chat.id
                where_opt &= Q(id__lte=current)

        limit = size

        chats = await Chat.objects.filter(where_opt).order_by("-id")[:limit]
        count = await Chat.objects.filter(where_opt).count()

        promise_list = []
        for message in chats:
            if message.user_id:
                item = message
                user = await user_service.get_one_user_info({'id': message.user_id})
                item.nick_name = user.nick_name
                item.avatar = user.avatar
                promise_list.append(item)

        list_of_chats = await Promise.all(promise_list)

        return {
            'current': current,
            'size': len(list_of_chats),
            'total': count,
            'list': list_of_chats[::-1],  # 反转列表
        }


# 创建服务实例
chat_service = ChatService()
