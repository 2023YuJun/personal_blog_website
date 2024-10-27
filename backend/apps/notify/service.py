from django.db.models import Q
from django.utils import timezone
from django.db import transaction
from .serializers import *


def create_notify(notify):
    """
    新增消息通知
    """
    with transaction.atomic():
        current_time = timezone.localtime()
        notify = Notify.objects.create(**notify, createdAt=current_time, updatedAt=current_time)
        serialize_notify = NotifySerializer(notify, many=True).data
    return serialize_notify


def update_notify(id):
    """
    已阅消息通知
    """
    current_time = timezone.localtime()
    res = Notify.objects.filter(id=id).update(isView=2, updatedAt=current_time)
    return res > 0


def delete_notifys(id):
    """
    删除消息通知
    """
    res = Notify.objects.filter(id=id).delete()
    return res


def get_notify_list(current, size, user_id):
    """
    获取当前用户的消息推送
    """
    where_opt = Q()
    if user_id:
        where_opt &= Q(user_id=user_id)

    offset = (current - 1) * size
    rows = Notify.objects.filter(where_opt).order_by("isView", "-createdAt")[offset:offset + size]
    total_count = Notify.objects.filter(where_opt).count()
    rows = NotifySerializer(rows, many=True).data
    return {
        "current": current,
        "size": size,
        "total": total_count,
        "list": rows,
    }

