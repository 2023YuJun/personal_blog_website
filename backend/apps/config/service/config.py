from ..models import Config  # 根据你的项目结构调整导入路径
from django.db import transaction


class ConfigService:
    """
    网站设置服务层
    """

    async def update_config(self, config):
        """
        更新配置
        """
        config_id = config.get('id')
        one = await Config.objects.filter(id=config_id).first()

        if one:
            async with transaction.atomic():
                await Config.objects.filter(id=config_id).update(**config)
        else:
            async with transaction.atomic():
                await Config.objects.create(**config)

        return bool(one)

    async def get_config(self):
        """
        获取配置
        """
        res = await Config.objects.all()
        return res[0] if res else False

    async def add_view(self):
        """
        增加访问次数
        """
        res = await Config.objects.all()
        if res:
            config = await Config.objects.filter(id=res[0].id).first()
            if config:
                await config.view_time.increment()  # 假设你在 Config 模型中有 view_time 字段
                return "添加成功"
        return "需要初始化"


# 创建服务实例
config_service = ConfigService()
