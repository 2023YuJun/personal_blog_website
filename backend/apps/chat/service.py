from .models import Chat
from .serializers import ChatSerializer
from django.db.models import Q
from django.utils import timezone


def create_chat(chat):
    """
    新增聊天
    """
    current_time = timezone.localtime()
    chat_obj = Chat.objects.create(
        content_type=chat.get('content_type'),
        content=chat.get('content'),
        user_id=chat.get('user_id'),
        createdAt=current_time,
        updatedAt=current_time
    )
    return chat_obj


def delete_chats():
    """
    删除所有聊天记录
    """
    res = Chat.objects.all().delete()
    return res


def delete_one_chat(chat_id, user_id):
    """
    删除单条聊天记录（撤销聊天）
    """
    res = Chat.objects.filter(id=chat_id, user_id=user_id).delete()
    return res


def get_one_chat(chat_id):
    """
    根据id获取聊天信息
    """
    res = Chat.objects.filter(id=chat_id).first()
    return res if res else None


def get_all_chats():
    """
    获取所有的聊天记录
    """
    res = Chat.objects.filter(content_type="image").values("content")
    return list(res)


def get_chat_list(params):
    """
    分页获取聊天列表（同步）
    """
    size = params.get('size', 10)
    current = params.get('current', 1)
    last_id = params.get('last_id')

    where_opt = Q()

    # 构建查询条件
    if last_id:
        where_opt &= Q(id__lt=last_id)
        current = last_id
    else:
        last_chat = Chat.objects.order_by("-id").first()  # 同步查询
        if last_chat:
            current = last_chat.id
            where_opt &= Q(id__lte=current)

    limit = size

    # 获取聊天列表，按ID降序排列
    chats = Chat.objects.filter(where_opt).order_by("-id")[:limit]
    count = Chat.objects.filter(where_opt).count()  # 同步计数

    # 将聊天记录反转，并返回
    reversed_chats = list(chats)[::-1]
    serialized_chats = ChatSerializer(reversed_chats, many=True).data
    return {
        'current': current,
        'size': size,
        'total': count,
        'list': serialized_chats,
    }
