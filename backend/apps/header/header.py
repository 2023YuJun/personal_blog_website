from apps.header.models import Header
from django.db import transaction


def add_or_update_header(header_data):
    """
    新增 / 修改 背景
    """
    header_id = header_data.get('id')
    if header_id:
        with transaction.atomic():
            Header.objects.filter(id=header_id).update(
                route_name=header_data['route_name'],
                bg_url=header_data['bg_url']
            )
    else:
        with transaction.atomic():
            Header.objects.create(
                route_name=header_data['route_name'],
                bg_url=header_data['bg_url']
            )
    return True


def delete_header(header_id):
    """
    根据id删除背景
    """
    res = Header.objects.filter(id=header_id).delete()
    return res[0] if res else None


def get_all_headers():
    """
    获取所有背景
    """
    headers = Header.objects.all().values('id', 'route_name', 'bg_url')
    return headers


def get_one_by_path(route_name):
    """
    根据 route_name 获取背景
    """
    header = Header.objects.filter(route_name=route_name).first()
    return header if header else None
