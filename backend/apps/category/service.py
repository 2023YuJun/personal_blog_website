from apps.category.models import Category
from .serializers import CategorySerializer
from django.db.models import Q
from rest_framework.response import Response
from django.utils import timezone
from utils.result import ERRORCODE, throw_error

error_code = ERRORCODE['CATEGORY']


def create_category(category):
    """
    新增分类
    """
    category_name = category.get('category_name')
    current_time = timezone.localtime()
    category_obj = Category.objects.create(category_name=category_name, createdAt=current_time, updatedAt=current_time)
    return category_obj


def update_category(category):
    """
    修改分类
    """
    category_id = category.get('id')
    category_name = category.get('category_name')
    current_time = timezone.localtime()
    res = Category.objects.filter(id=category_id).update(category_name=category_name, updatedAt=current_time)
    return res > 0


def delete_categories(category):
    """
    删除分类
    """
    id_list = category.get('categoryIdList')
    res, _ = Category.objects.filter(id__in=id_list).delete()
    return res


def get_one_category(category):
    """
    根据id或者分类名称获取分类信息
    """
    query = Q()

    if category.get('id'):
        query &= Q(id=category['id'])

    if category.get('category_name'):
        query &= Q(category_name=category['category_name'])

    if not query:
        return None
    res = Category.objects.filter(query).values('id', 'category_name').first()

    return res if res else None


def get_category_name_by_id(category_id):
    """
    通过分类id获取分类名称
    """
    category = Category.objects.filter(pk=category_id).first()
    return category.category_name if category else None


def get_category_list(category):
    """
    分页获取分类列表
    """

    current = category.get('current', 1)
    size = category.get('size', 10)
    category_name = category.get('category_name', None)

    query = Q()
    if category_name:
        query &= Q(category_name__icontains=category_name)

    offset = (current - 1) * size
    categories = Category.objects.filter(query)[offset:offset + size]
    categories = CategorySerializer(categories, many=True).data
    count = Category.objects.filter(query).count()
    return {
        'current': current,
        'size': size,
        'total': count,
        'list': categories,
    }


def get_category_dictionary():
    """
    获取分类数据字典
    """
    categories = Category.objects.values('id', 'category_name')
    return categories if categories else None


def get_category_count():
    """
    获取分类总数
    """
    count = Category.objects.count()
    return count


def verify_category(category):
    """
    校验分类
    """
    category_name = category.get('category_name')
    category_id = category.get('id')

    if not category_name:
        print("分类名称不能为空")
        return Response(throw_error(error_code, "分类名称不能为空"), status=400)

    res = get_one_category({'category_name': category_name})
    if res and res['id'] == category_id:
        print("分类已存在")
        return Response(throw_error(error_code, "分类已存在"), status=400)

    return None


def verify_delete_categories(category):
    """
    校验删除分类
    """
    category_id_list = category.get('categoryIdList', [])

    if not category_id_list:
        print("分类id列表不能为空")
        return Response(throw_error(error_code, "分类id列表不能为空"), status=400)

    return None
