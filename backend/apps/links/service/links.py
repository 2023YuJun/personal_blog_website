from ..models import Links  # 根据你的项目结构调整导入路径
from django.db.models import Q


class LinksService:
    """
    友链服务层
    """

    async def add_or_update_links(self, link_data):
        """
        新增/编辑友链
        """
        id = link_data.get('id')
        if id:
            await Links.objects.filter(id=id).update(**link_data)
        else:
            link_data['status'] = 1  # 默认状态
            await Links.objects.create(**link_data)

        return True

    async def delete_links(self, id_list):
        """
        批量删除友链
        """
        res = await Links.objects.filter(id__in=id_list).delete()
        return res if res else None

    async def approve_links(self, id_list):
        """
        批量审核友链
        """
        res = await Links.objects.filter(id__in=id_list).update(status=2)
        return res if res else None

    async def get_links_list(self, current, size, time=None, status=None, site_name=None):
        """
        分页获取友链
        """
        offset = (current - 1) * size
        where_opt = Q()

        if site_name:
            where_opt &= Q(site_name__icontains=site_name)
        if status:
            where_opt &= Q(status=status)
        if time:
            where_opt &= Q(createdAt__range=time)

        total_count = await Links.objects.filter(where_opt).count()
        rows = await Links.objects.filter(where_opt).order_by("createdAt")[offset:offset + size]

        return {
            'current': current,
            'size': size,
            'list': rows,
            'total': total_count,
        }


# 创建服务实例
links_service = LinksService()
