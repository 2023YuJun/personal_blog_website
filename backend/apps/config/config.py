from apps.config.models import Config
from django.db import transaction


def update_config(config):
    """
    更新配置
    """
    config_id = config.get('id')
    one = Config.objects.filter(id=config_id).first()

    if one:
        with transaction.atomic():
            Config.objects.filter(id=config_id).update(**config)
    else:
        with transaction.atomic():
            Config.objects.create(**config)

    return bool(one)


def get_config():
    """
    获取配置
    """
    res = Config.objects.all()
    return res[0] if res else False


def add_view():
    """
    增加访问次数
    """
    res = Config.objects.all()
    if res:
        config = Config.objects.filter(id=res[0].id).first()
        if config:
            config.view_time.increment()
            return "添加成功"
    return "需要初始化"
