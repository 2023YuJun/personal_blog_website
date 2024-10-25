from django.utils import timezone
from .models import PhotoAlbum
from apps.photo.photo_service import delete_photos_by_album_id
from .serializers import PhotoAlbumSerializer


def add_album(album_name, album_cover, description):
    """
    新增相册
    """
    current_time = timezone.localtime()
    res = PhotoAlbum.objects.create(album_name=album_name, album_cover=album_cover, description=description,
                                    createdAt=current_time, updatedAt=current_time)
    res = PhotoAlbumSerializer(res, many=True).data
    return res


def delete_album(id):
    """
    根据id删除相册
    """
    res = PhotoAlbum.objects.filter(id=id).delete()
    # 删除相册下的图片
    delete_photos_by_album_id(id)
    return res > 0


def update_album(id, album_name, album_cover, description):
    """
    编辑相册
    """
    current_time = timezone.localtime()
    res = PhotoAlbum.objects.filter(id=id).update(album_name=album_name, album_cover=album_cover,
                                                  description=description, updatedAt=current_time)
    return res > 0


def get_album_list(current, size, album_name=None):
    """
    获取相册列表
    """
    offset = size * (current - 1)
    limit = size

    where_opt = {}
    if album_name:
        where_opt['album_name__icontains'] = album_name

    rows = PhotoAlbum.objects.filter(**where_opt)[offset:offset + limit]
    total_count = PhotoAlbum.objects.filter(**where_opt).count()
    rows = PhotoAlbumSerializer(rows, many=True).data

    return {
        "current": current,
        "size": size,
        "list": rows,
        "total": total_count,
    }


def get_one_album(id=None, album_name=None):
    """
    根据id或相册名称获取相册信息
    """
    where_opt = {}
    if id:
        where_opt['id'] = id
    if album_name:
        where_opt['album_name'] = album_name

    res = PhotoAlbum.objects.filter(**where_opt).first()
    return res


def get_all_album_list():
    """
    获取所有的相册
    """
    res = PhotoAlbum.objects.all().order_by('-createdAt')
    res = PhotoAlbumSerializer(res, many=True).data
    return res


