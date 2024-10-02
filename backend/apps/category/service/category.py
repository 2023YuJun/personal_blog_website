from ..models import Category
from django.db.models import Q


class CategoryService:
    """
    分类服务层
    """

    async def create_category(self, category):
        """
        新增分类
        """
        category_name = category.get('category_name')
        category_obj = await Category.objects.create(category_name=category_name)
        return category_obj

    async def update_category(self, category):
        """
        修改分类
        """
        category_id = category.get('id')
        category_name = category.get('category_name')
        res = await Category.objects.filter(id=category_id).update(category_name=category_name)
        return res > 0

    async def delete_categories(self, id_list):
        """
        删除分类
        """
        res = await Category.objects.filter(id__in=id_list).delete()
        return res[0]  # 返回删除的条数

    async def get_one_category(self, filters):
        """
        根据id或者分类名称获取分类信息
        """
        query = Q()
        if 'id' in filters:
            query &= Q(id=filters['id'])
        if 'category_name' in filters:
            query &= Q(category_name=filters['category_name'])

        res = await Category.objects.filter(query).values('id', 'category_name').first()
        return res if res else None

    async def get_category_name_by_id(self, category_id):
        """
        通过分类id获取分类名称
        """
        category = await Category.objects.get(pk=category_id)
        return category.category_name if category else None

    async def get_category_list(self, params):
        """
        分页获取分类列表
        """
        current = params.get('current', 1)
        size = params.get('size', 10)
        category_name = params.get('category_name', None)

        query = Q()
        if category_name:
            query &= Q(category_name__icontains=category_name)

        offset = (current - 1) * size
        categories = await Category.objects.filter(query)[offset:offset + size]
        count = await Category.objects.filter(query).count()

        return {
            'current': current,
            'size': size,
            'total': count,
            'list': categories,
        }

    async def get_category_dictionary(self):
        """
        获取分类数据字典
        """
        categories = await Category.objects.values('id', 'category_name')
        return categories if categories else None

    async def get_category_count(self):
        """
        获取分类总数
        """
        count = await Category.objects.count()
        return count


# 创建服务实例
category_service = CategoryService()
