from apps.photo.models import Photo  # 根据你的项目结构调整导入路径


def add_photos(photo_list):
    """
    批量新增图片
    """
    res = Photo.objects.bulk_create([Photo(**photo) for photo in photo_list])
    return res


def delete_photos(id_list, type):
    """
    批量删除图片
    """
    if int(type) == 1:
        res = Photo.objects.filter(id__in=id_list).update(status=2)
    else:
        res = Photo.objects.filter(id__in=id_list).delete()

    return res


def revert_photos(id_list):
    """
    批量恢复图片
    """
    res = Photo.objects.filter(id__in=id_list).update(status=1)
    return res


def get_photos_by_album_id(current, size, album_id, status):
    """
    获取图片列表
    """
    offset = size * (current - 1)
    limit = size

    rows = Photo.objects.filter(album_id=album_id, status=status)[offset:offset + limit]
    total_count = Photo.objects.filter(album_id=album_id, status=status).count()

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
