from apps.message.models import Message
from apps.user.service import get_one_user_info
from apps.like.service import get_is_like_by_ip_and_type, get_is_like_by_id_and_type
from apps.comment.service import get_comment_total
from django.db.models import Q, F


def add_message(message_data):
    """
    发布留言
    """
    Message.objects.create(**message_data)
    return True


def update_message(id, message):
    """
    修改留言
    """
    Message.objects.filter(id=id).update(message)
    return True


def delete_message(id_list):
    """
    根据id列表删除留言
    """
    res = Message.objects.filter(id__in=id_list).delete()
    return res if res else None


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

    # 根据用户form_id获取用户当前的昵称和头像
    for row in rows:
        if row.user_id:
            user_info = get_one_user_info({"id": row.user_id})
            row.nick_name = user_info.get('nick_name', '')
            row.avatar = user_info.get('avatar', '')
        else:
            row.nick_name = ''
            row.avatar = ''

    # 判断当前登录用户是否点赞了
    if user_id:
        for row in rows:
            row.is_like = get_is_like_by_id_and_type(row.id, 3, user_id)
    else:
        for row in rows:
            row.is_like = get_is_like_by_ip_and_type(row.id, 3, ip)

    # 获取每一条的评论条数
    for row in rows:
        row.comment_total = get_comment_total(row.id, 3)

    return {
        "current": current,
        "size": size,
        "list": rows,
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

    # 按照出现次数排序并返回前10个
    sorted_tags = sorted(tag_counts.items(), key=lambda item: item[1], reverse=True)
    return [{"tag": tag, "count": count} for tag, count in sorted_tags[:10]]
