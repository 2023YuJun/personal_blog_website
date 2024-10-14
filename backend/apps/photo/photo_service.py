from django.db import transaction
from django.utils import timezone

from .serializers import *


def add_photos(photo_list):
    """
    批量新增图片
    """
    current_time = timezone.localtime()
    photos_to_create = []

    for photo in photo_list:
        photo['createdAt'] = current_time
        photo['updatedAt'] = current_time
        photos_to_create.append(Photo(**photo))

    with transaction.atomic():
        res = Photo.objects.bulk_create(photos_to_create)

    return res


def delete_photos(id_list, type):
    """
    批量删除图片
    """
    if int(type) == 1:
        current_time = timezone.localtime()
        res = Photo.objects.filter(id__in=id_list).update(status=2, updatedAt=current_time)
    else:
        res = Photo.objects.filter(id__in=id_list).delete()

    return res


def revert_photos(id_list):
    """
    批量恢复图片
    """
    current_time = timezone.localtime()
    res = Photo.objects.filter(id__in=id_list).update(status=1, updatedAt=current_time)
    return res


def get_photos_by_album_id(current, size, album_id, status):
    """
    获取图片列表
    """
    offset = size * (current - 1)
    limit = size

    rows = Photo.objects.filter(album_id=album_id, status=status)[offset:offset + limit]
    total_count = Photo.objects.filter(album_id=album_id, status=status).count()
    rows = PhotoSerializer(rows, many=True).data

    return {
        "current": current,
        "size": size,
        "list": rows,
        "total": total_count,
    }


def delete_photos_by_album_id(album_id):
    """
    根据相册id删除图片
    """
    res = Photo.objects.filter(album_id=album_id).delete()
    return res


def get_all_photos_by_album_id(album_id):
    """
    获取所有可用的图片
    """
    res = Photo.objects.filter(album_id=album_id, status=1).order_by('-createdAt')
    return res
