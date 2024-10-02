from ..models import PhotoAlbum  # 根据你的项目结构调整导入路径
from .photo import photo_service  # 根据项目结构调整导入路径


class PhotoAlbumService:
    """
    相册服务层
    """

    async def add_album(self, album_name, album_cover, description):
        """
        新增相册
        """
        res = await PhotoAlbum.objects.create(album_name=album_name, album_cover=album_cover, description=description)
        return res

    async def delete_album(self, id):
        """
        根据id删除相册
        """
        res = await PhotoAlbum.objects.filter(id=id).delete()
        # 删除相册下的图片
        await photo_service.delete_photos_by_album_id(id)
        return res > 0

    async def update_album(self, id, album_name, album_cover, description):
        """
        编辑相册
        """
        res = await PhotoAlbum.objects.filter(id=id).update(album_name=album_name, album_cover=album_cover,
                                                            description=description)
        return res > 0

    async def get_album_list(self, current, size, album_name=None):
        """
        获取相册列表
        """
        offset = size * (current - 1)
        limit = size

        where_opt = {}
        if album_name:
            where_opt['album_name__icontains'] = album_name

        rows = await PhotoAlbum.objects.filter(**where_opt)[offset:offset + limit]
        total_count = await PhotoAlbum.objects.filter(**where_opt).count()

        return {
            "current": current,
            "size": size,
            "list": rows,
            "total": total_count,
        }

    async def get_one_album(self, id=None, album_name=None):
        """
        根据id或相册名称获取相册信息
        """
        where_opt = {}
        if id:
            where_opt['id'] = id
        if album_name:
            where_opt['album_name'] = album_name

        res = await PhotoAlbum.objects.filter(**where_opt).first()
        return res

    async def get_all_album_list(self):
        """
        获取所有的相册
        """
        res = await PhotoAlbum.objects.all().order_by('-createdAt')
        return res


# 创建服务实例
photo_album_service = PhotoAlbumService()
