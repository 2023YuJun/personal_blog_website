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


def get_minio_client():
    global minio_client
    if not minio_client:
        if MINIO_PATH and MINIO_ACCESSKEY and MINIO_SECRETKEY:
            try:
                end_point = f"{MINIO_PATH}:{MINIO_PORT}"
                minio_client = Minio(
                    end_point,
                    access_key=MINIO_ACCESSKEY,
                    secret_key=MINIO_SECRETKEY,
                    secure=False
                )
            except Exception as err:
                print(f"Minio client 初始化失败: {err}")
                raise err
        else:
            raise ValueError("请在 settings 中完善 Minio 配置项")
    return minio_client


# 生成随机文件名
def generate_random_file_name(length=12):
    chars = string.ascii_letters
    return ''.join(random.choice(chars) for _ in range(length))


# 判断 bucket 是否存在
def bucket_exists():
    try:
        client = get_minio_client()
        return client.bucket_exists(MINIO_BUCKET)
    except Exception as err:
        print(f"Bucket 检查失败: {err}")
        return False


# 上传文件
def upload(file):
    meta_data = {
        "Content-Type": file.content_type,
        "X-Amz-Meta-Testing": "1234",
        "example": "5678",
    }

    file_name = generate_random_file_name()

    try:
        client = get_minio_client()
        client.put_object(
            bucket_name=MINIO_BUCKET,
            object_name=file_name,
            data=file.file,
            length=file.size,
            content_type=file.content_type,
            metadata=meta_data
        )
        return f"/blog-images/{file_name}"
    except Exception as err:
        print(f"文件上传失败: {err}")
        return False


def delete_minio_imgs(img_list):
    try:
        client = get_minio_client()
        for img in img_list:
            client.remove_object(MINIO_BUCKET, img)
    except Exception as err:
        print(f"删除图片失败: {err}")


def minio_upload(file):
    try:
        if not bucket_exists():
            print("Bucket 不存在")
            return False

        url = upload(file)
        return url if url else False
    except Exception as err:
        print(f"Minio 上传失败: {err}")
        return False
