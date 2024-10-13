import random
import string

from django.conf import settings
from minio import Minio

# MinIO 配置
MINIO_ACCESSKEY = settings.MINIO_ACCESSKEY
MINIO_SECRETKEY = settings.MINIO_SECRETKEY
MINIO_BUCKET = settings.MINIO_BUCKET
MINIO_PATH = settings.MINIO_PATH
MINIO_PORT = settings.MINIO_PORT or 9000

minio_client = None


if MINIO_PATH and MINIO_ACCESSKEY and MINIO_SECRETKEY:
    try:
        minio_client = Minio(
            MINIO_PATH,
            access_key=MINIO_ACCESSKEY,
            secret_key=MINIO_SECRETKEY,
            secure=False
        )
    except Exception as err:
        print(err)
else:
    print("请在settings中完善minio配置项")


# 生成随机文件名
def generate_random_file_name(length=12):
    chars = string.ascii_letters  # 包含所有英文字母及其大写形式
    return ''.join(random.choice(chars) for _ in range(length))


async def bucket_exists():
    # 判断 bucket 是否存在
    try:
        return minio_client.bucket_exists(MINIO_BUCKET)
    except Exception as err:
        print(err)
        return False


async def upload(file_path):
    meta_data = {
        "Content-Type": "application/octet-stream",
        "X-Amz-Meta-Testing": 1234,
        "example": 5678,
    }

    file_name = generate_random_file_name()

    try:
        minio_client.fput_object(MINIO_BUCKET, file_name, file_path, meta_data)
        return f"/blog-images/{file_name}"
    except Exception as err:
        print(err)
        return False


def delete_minio_imgs(img_list):
    for img in img_list:
        try:
            minio_client.remove_object(MINIO_BUCKET, img)
        except Exception as err:
            print(err)


async def minio_upload(file_path):
    try:
        exist = await bucket_exists()
        if not exist:
            print("bucket不存在")
            return

        url = await upload(file_path)
        return url if url else False
    except Exception as err:
        print(err)
