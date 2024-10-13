from apps.talk.models import TalkPhoto
from utils.minioUpload import delete_minio_imgs


def publish_talk_photo(img_list):
    """
    新增说说图片
    """
    res = TalkPhoto.objects.bulk_create([TalkPhoto(**img) for img in img_list])
    return res


def delete_talk_photo(talk_id):
    """
    根据说说id删除图片
    """
    url_list = TalkPhoto.objects.filter(talk_id=talk_id).values_list('url', flat=True)

    # 远程删除图片
    keys = [url.split("/")[-1] for url in url_list]
    delete_minio_imgs(keys)

    res = TalkPhoto.objects.filter(talk_id=talk_id).delete()
    return res


def get_photo_by_talk_id(talk_id):
    """
    根据说说id获取图片列表
    """
    res = TalkPhoto.objects.filter(talk_id=talk_id).values('talk_id', 'url')

    return list(res)  # 直接返回查询结果

