from ..models import TalkPhoto
# from backend.settings import UPLOADTYPE
# from utils.qiniuUpload import delete_imgs
# from controller.utils.index import delete_online_imgs
from utils.minioUpload import delete_minio_imgs


class TalkPhotoService:
    """
    说说图片服务层
    """

    async def publish_talk_photo(self, img_list):
        """
        新增说说图片
        """
        res = await TalkPhoto.objects.bulk_create([TalkPhoto(**img) for img in img_list])
        return res

    async def delete_talk_photo(self, talk_id):
        """
        根据说说id删除图片
        """
        url_list = await TalkPhoto.objects.filter(talk_id=talk_id).values_list('url', flat=True)

        # 远程删除图片
        keys = [url.split("/")[-1] for url in url_list]
        # if UPLOADTYPE == "qiniu":
        #     await delete_imgs(keys)
        # elif UPLOADTYPE == "online":
        #     await delete_online_imgs(keys)
        # elif UPLOADTYPE == "minio":
        await delete_minio_imgs(keys)

        res = await TalkPhoto.objects.filter(talk_id=talk_id).delete()
        return res

    async def get_photo_by_talk_id(self, talk_id):
        """
        根据说说id获取图片列表
        """
        res = await TalkPhoto.objects.filter(talk_id=talk_id).values('talk_id', 'url')

        return list(res)  # 直接返回查询结果


# 创建服务实例
talk_photo_service = TalkPhotoService()
