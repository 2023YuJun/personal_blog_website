from ..models import Notify  # 根据你的项目结构调整导入路径
from django.db.models import Q


class NotifyService:
    """
    消息通知服务层
    """

    async def create_notify(self, notify):
        """
        新增消息通知
        """
        notify_instance = await Notify.objects.create(**notify)
        return notify_instance

    async def update_notify(self, id):
        """
        已阅消息通知
        """
        res = await Notify.objects.filter(id=id).update(isView=2)
        return res > 0

    async def delete_notifys(self, id):
        """
        删除消息通知
        """
        res = await Notify.objects.filter(id=id).delete()
        return res

    async def get_notify_list(self, current, size, user_id):
        """
        获取当前用户的消息推送
        """
        where_opt = Q()
        if user_id:
            where_opt &= Q(user_id=user_id)

        offset = (current - 1) * size
        rows = await Notify.objects.filter(where_opt).order_by("isView", "-createdAt")[offset:offset + size]
        total_count = await Notify.objects.filter(where_opt).count()

        return {
            "current": current,
            "size": size,
            "total": total_count,
            "list": rows,
        }


# 创建服务实例
notify_service = NotifyService()
