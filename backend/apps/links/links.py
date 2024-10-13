from apps.links.models import Links  # 根据你的项目结构调整导入路径
from django.db.models import Q


def add_or_update_links(link_data):
    """
    新增/编辑友链
    """
    id = link_data.get('id')
    if id:
        Links.objects.filter(id=id).update(**link_data)
    else:
        link_data['status'] = 1  # 默认状态
        Links.objects.create(**link_data)

    return True


def delete_links(id_list):
    """
    批量删除友链
    """
    res = Links.objects.filter(id__in=id_list).delete()
    return res if res else None


def approve_links(id_list):
    """
    批量审核友链
    """
    res = Links.objects.filter(id__in=id_list).update(status=2)
    return res if res else None


def get_links_list(current, size, time=None, status=None, site_name=None):
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

    total_count = Links.objects.filter(where_opt).count()
    rows = Links.objects.filter(where_opt).order_by("createdAt")[offset:offset + size]

    return {
        'current': current,
        'size': size,
        'list': rows,
        'total': total_count,
    }
