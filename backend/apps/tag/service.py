from django.db.models import Q
from rest_framework.response import Response
from django.utils import timezone
from utils.result import throw_error, ERRORCODE
from apps.tag.models import Tag
from .serializers import TagSerializer

error_code = ERRORCODE['TAG']


def create_tag(tag):
    """
    新增标签
    """
    tag_name = tag.get('tag_name')
    current_time = timezone.localtime()
    res = Tag.objects.create(tag_name=tag_name, createdAt=current_time, updatedAt=current_time)
    return res


def update_tag(tag):
    """
    修改标签
    """
    current_time = timezone.localtime()
    id = tag.get('id')
    tag_name = tag.get('tag_name')
    res = Tag.objects.filter(id=id).update(tag_name=tag_name, updatedAt=current_time)
    return res > 0


def delete_tags(tag):
    """
    删除标签
    """
    id_list = tag.get('tagIdList')
    res = Tag.objects.filter(id__in=id_list).delete()
    return res


def get_one_tag(id=None, tag_name=None):
    """
    根据id或者标签名称获取标签信息
    """
    where_opt = Q()

    if id and tag_name:
        where_opt &= Q(id=id) & Q(tag_name=tag_name)
    else:
        if id:
            where_opt &= Q(id=id)
        if tag_name:
            where_opt &= Q(tag_name=tag_name)
    res = Tag.objects.filter(where_opt).values('id', 'tag_name').first()
    return res


def get_tag_list(tag):
    """
    获取标签列表
    """
    current = tag.get('current')
    size = tag.get('size')
    tag_name = tag.get('tag_name')
    offset = size * (current - 1)

    where_opt = Q()
    if tag_name:
        where_opt &= Q(tag_name__icontains=tag_name)

    rows = Tag.objects.filter(where_opt)[offset:offset + size]
    rows = TagSerializer(rows, many=True).data
    total_count = Tag.objects.filter(where_opt).count()
    return {
        "current": current,
        "size": size,
        "total": total_count,
        "list": rows,
    }


def get_tag_by_tag_id_list(tag_id_list):
    """
    根据tag_id列表获取tag列表
    """
    tag_list = Tag.objects.filter(id__in=tag_id_list).values('id', 'tag_name')
    tag_name_list = [v['tag_name'] for v in tag_list]

    return {
        "tagNameList": tag_name_list,
        "tagList": tag_list,
    }


def get_tag_dictionary():
    """
    字典，用于反显tag
    """
    tags = Tag.objects.values('id', 'tag_name')
    return tags if tags else None


def get_tag_count():
    """
    获取标签总数
    """
    res = Tag.objects.count()
    return res


def verify_tag(tag):
    id = tag.get('id')
    tag_name = tag.get('tag_name')
    if not tag_name:
        print("标签名称不能为空")
        return Response(throw_error(error_code, "标签名称不能为空"), status=400)

    res = get_one_tag(id, tag_name)
    if res:
        print("标签已存在")
        return Response(throw_error(error_code, "标签已存在"), status=400)

    return None


def verify_delete_tags(tag):
    tag_id_list = tag.get('tagIdList')
    if not tag_id_list:
        print("标签id列表不能为空")
        return Response(throw_error(error_code, "标签id列表不能为空"), status=400)

    return None
