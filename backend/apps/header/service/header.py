from ..models import Header  # 根据你的项目结构调整导入路径
from django.db import transaction


class HeaderService:
    """
    头部背景图服务层
    """

    async def add_or_update_header(self, header_data):
        """
        新增 / 修改 背景
        """
        header_id = header_data.get('id')
        if header_id:
            async with transaction.atomic():
                await Header.objects.filter(id=header_id).update(
                    route_name=header_data['route_name'],
                    bg_url=header_data['bg_url']
                )
        else:
            async with transaction.atomic():
                await Header.objects.create(
                    route_name=header_data['route_name'],
                    bg_url=header_data['bg_url']
                )
        return True

    async def delete_header(self, header_id):
        """
        根据id删除背景
        """
        res = await Header.objects.filter(id=header_id).delete()
        return res[0] if res else None

    async def get_all_headers(self):
        """
        获取所有背景
        """
        headers = await Header.objects.all().values('id', 'route_name', 'bg_url')
        return list(headers)

    async def get_one_by_path(self, route_name):
        """
        根据 route_name 获取背景
        """
        header = await Header.objects.filter(route_name=route_name).first()
        return header if header else None


# 创建服务实例
header_service = HeaderService()
