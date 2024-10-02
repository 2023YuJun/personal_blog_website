from ..models import Tag  # 根据你的项目结构调整导入路径
from django.db.models import Q


class TagService:
    """
    标签服务层
    """

    async def create_tag(self, tag_name):
        """
        新增标签
        """
        res = await Tag.objects.create(tag_name=tag_name)
        return res

    async def update_tag(self, id, tag_name):
        """
        修改标签
        """
        res = await Tag.objects.filter(id=id).update(tag_name=tag_name)
        return res > 0

    async def delete_tags(self, id_list):
        """
        删除标签
        """
        res = await Tag.objects.filter(id__in=id_list).delete()
        return res

    async def get_one_tag(self, id=None, tag_name=None):
        """
        根据id或者标签名称获取标签信息
        """
        where_opt = Q()
        if id:
            where_opt |= Q(id=id)
        if tag_name:
            where_opt |= Q(tag_name=tag_name)

        res = await Tag.objects.filter(where_opt).values('id', 'tag_name').first()
        return res

    async def get_tag_list(self, current, size, tag_name=None):
        """
        获取标签列表
        """
        offset = size * (current - 1)
        limit = size

        where_opt = Q()
        if tag_name:
            where_opt &= Q(tag_name__icontains=tag_name)

        rows = await Tag.objects.filter(where_opt)[offset:offset + limit]
        total_count = await Tag.objects.filter(where_opt).count()

        return {
            "current": current,
            "size": size,
            "total": total_count,
            "list": rows,
        }

    async def get_tag_by_tag_id_list(self, tag_id_list):
        """
        根据tag_id列表获取tag列表
        """
        res = await Tag.objects.filter(id__in=tag_id_list).values('id', 'tag_name')
        tag_name_list = [v['tag_name'] for v in res]

        return {
            "tagNameList": tag_name_list,
            "tagList": res,
        }

    async def get_tag_dictionary(self):
        """
        字典，用于反显tag
        """
        res = await Tag.objects.values('id', 'tag_name')
        return res

    async def get_tag_count(self):
        """
        获取标签总数
        """
        res = await Tag.objects.count()
        return res


# 创建服务实例
tag_service = TagService()
