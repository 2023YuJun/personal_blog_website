from apps.notify.models import Notify  # 根据你的项目结构调整导入路径
from django.db.models import Q


def create_notify(notify):
    """
    新增消息通知
    """
    notify_instance = Notify.objects.create(**notify)
    return notify_instance


def update_notify(id):
    """
    已阅消息通知
    """
    res = Notify.objects.filter(id=id).update(isView=2)
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

    return {
        "current": current,
        "size": size,
        "total": total_count,
        "list": rows,
    }

