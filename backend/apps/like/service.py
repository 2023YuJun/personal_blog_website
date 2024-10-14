from apps.like.models import Like
from django.utils import timezone


def add_like(like_data):
    """
    点赞
    """
    current_time = timezone.localtime()
    Like.objects.create(**like_data, createdAt=current_time, updatedAt=current_time)
    return True


def cancel_like(for_id, type, user_id=None, ip=None):
    """
    根据 for_id、type、user_id 取消点赞
    """
    where_opt = {'for_id': for_id, 'type': type}
    if ip:
        where_opt['ip'] = ip
    if user_id:
        where_opt['user_id'] = user_id

    res = Like.objects.filter(**where_opt).delete()
    return res if res else None


def get_is_like_by_id_and_type(for_id, type, user_id):
    """
    获取当前用户对当前文章/说说/留言是否点赞
    """
    like_exists = Like.objects.filter(for_id=for_id, type=type, user_id=user_id).exists()
    return like_exists


def get_is_like_by_ip_and_type(for_id, type, ip):
    """
    获取当前ip对当前文章/说说/留言是否点赞
    """
    like_exists = Like.objects.filter(for_id=for_id, type=type, ip=ip).exists()
    return like_exists
