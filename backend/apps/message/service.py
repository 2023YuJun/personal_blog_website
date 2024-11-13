from apps.message.models import Message
from apps.user.service import get_one_user_info
from apps.like.service import get_is_like_by_ip_and_type, get_is_like_by_id_and_type
from apps.comment.service import get_comment_total
from django.db.models import Q, F
from django.db import transaction
from django.utils import timezone
from .serializers import MessageSerializer


def add_message(message_data):
    """
    发布留言
    """
    valid_fields = {field.name for field in Message._meta.get_fields()}
    filtered_data = {key: value for key, value in message_data.items() if key in valid_fields and key != 'id'}
    with transaction.atomic():
        filtered_data['createdAt'] = timezone.localtime()
        filtered_data['updatedAt'] = timezone.localtime()
        message = Message.objects.create(**filtered_data)
        res = MessageSerializer(message).data
    return res


def update_message(id, message_data):
    """
    修改留言
    """
    valid_fields = {field.name for field in Message._meta.get_fields()}
    filtered_data = {
        key: value for key, value in message_data.items()
        if key in valid_fields and key not in ['createdAt', 'updatedAt']
    }
    filtered_data['updatedAt'] = timezone.localtime()
    with transaction.atomic():
        updated_count = Message.objects.filter(id=id).update(**filtered_data)
        return updated_count > 0


def delete_message(id_list):
    """
    根据id列表删除留言
    """
    deleted_count, _ = Message.objects.filter(id__in=id_list).delete()
    return deleted_count > 0


def message_like(id):
    """
    点赞留言
    """
    updated_count = Message.objects.filter(pk=id).update(like_times=F('like_times') + 1)
    return updated_count > 0


def cancel_message_like(id):
    """
    取消点赞留言
    """
    updated_count = Message.objects.filter(pk=id).update(like_times=F('like_times') - 1)
    return updated_count > 0


def get_message_list(request):
    """
    分页获取留言
    """
    data = request.data
    current = data.get('current', 1)
    size = data.get('size', 10)
    tag = data.get('tag', None)
    message = data.get('message', None)
    time = data.get('time', None)
    user_id = data.get('user_id', None)
    offset = (current - 1) * size
    where_opt = Q()
    ip = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get(
        'REMOTE_ADDR')
    ip = ip.split(":")[-1]
    if tag:
        where_opt &= Q(tag=tag)
    if message:
        where_opt &= Q(message__icontains=message)
    if time:
        where_opt &= Q(createdAt__range=time)

    rows = Message.objects.filter(where_opt).order_by("-createdAt")[offset:offset + size]
    total_count = Message.objects.filter(where_opt).count()
    serializer_rows = MessageSerializer(rows, many=True).data

    return {
        "current": current,
        "size": size,
        "list": serializer_rows,
        "total": total_count,
    }


def get_all_message():
    """
    获取所有留言
    """
    rows = Message.objects.order_by("-createdAt").all()

    for row in rows:
        if row.user_id:
            user_info = get_one_user_info({"id": row.user_id})
            row.nick_name = user_info.get('nick_name', '')
            row.avatar = user_info.get('avatar', '')
        else:
            row.nick_name = ''
            row.avatar = ''

    return {
        "list": rows,
        "total": len(rows),
    }


def get_message_tag():
    """
    获取热门的标签
    """
    all_messages = Message.objects.all()
    tag_counts = {}

    for message in all_messages:
        tag = message.tag
        if tag:
            if tag not in tag_counts:
                tag_counts[tag] = 0
            tag_counts[tag] += 1

    sorted_tags = sorted(tag_counts.items(), key=lambda item: item[1], reverse=True)
    return [{"tag": tag, "count": count} for tag, count in sorted_tags[:10]]
