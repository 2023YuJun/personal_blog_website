from django.db import transaction
from django.utils import timezone
from django.db.models import F
from .serializers import *


def update_config(config):
    """
    更新或创建配置
    """
    config_id = config.get('id')
    model_fields = {field.name for field in Config._meta.get_fields()}

    # 确保不包含 createdAt 和 updatedAt 字段
    valid_config = {key: value for key, value in config.items() if key in model_fields and key not in ['createdAt', 'updatedAt']}

    current_time = timezone.localtime()

    with transaction.atomic():
        res, created = Config.objects.get_or_create(
            id=config_id,
            defaults={**valid_config, 'createdAt': current_time, 'updatedAt': current_time}
        )

        if not created:
            for key, value in valid_config.items():
                setattr(res, key, value)
            res.updatedAt = current_time
            res.save()

    serializer = ConfigSerializer(res)
    return serializer.data


def get_config():
    """
    获取配置
    """
    res = Config.objects.all().first()
    if res:
        serializer = ConfigSerializer(res)
        return serializer.data
    return None


def add_view():
    """
    增加访问次数
    """
    res = Config.objects.all()
    if res:
        config = Config.objects.filter(id=res[0].id).update(view_time=F('view_time') + 1)
        if config:
            return "添加成功"
    return "需要初始化"
