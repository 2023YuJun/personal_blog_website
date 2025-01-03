from rest_framework.response import Response
from rest_framework.views import APIView

from apps.photo.photo_service import *
from utils.minioUpload import delete_minio_imgs
from utils.result import result, ERRORCODE, throw_error

error_code = ERRORCODE['PHOTO']


class PhotoView(APIView):
    def post(self, request, *args, **kwargs):
        if 'add' in request.path:
            return self.add_photos(request)
        elif 'getPhotoListByAlbumId' in request.path:
            return self.get_photos_by_album_id(request)

    def put(self, request, *args, **kwargs):
        if 'delete' in request.path:
            return self.delete_photos(request)
        elif 'revert' in request.path:
            return self.revert_photos(request)

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if 'getAllPhotosByAlbumId' in request.path:
            return self.get_all_photos_by_album_id(id)

    def add_photos(self, request):
        try:
            photo_list = request.data.get('photoList', [])
            res = add_photos(photo_list)
            return Response(result("新增图片成功", res), status=201)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "新增图片失败"), status=400)

    def delete_photos(self, request):
        try:
            img_list = request.data.get('imgList', [])
            type_ = request.data.get('type')
            id_list = [v['id'] for v in img_list]
            res = delete_photos(id_list, type_)

            # 远程删除图片
            keys = [v['url'].split("/")[-1] for v in img_list]
            if type_ == 2:
                delete_minio_imgs(keys)

            return Response(result("删除图片成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "删除图片失败"), status=400)

    def revert_photos(self, request):
        try:
            id_list = request.data.get('id_list', [])
            res = revert_photos(id_list)
            return Response(result("恢复图片成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "恢复图片失败"), status=400)

    def get_photos_by_album_id(self, request):
        try:
            current = request.data.get('current')
            size = request.data.get('size')
            album_id = request.data.get('id')
            status = request.data.get('status')
            res = get_photos_by_album_id(current, size, album_id, status)
            return Response(result("获取相册图片成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取相册图片失败"), status=400)

    def get_all_photos_by_album_id(self, album_id):
        try:
            res = get_all_photos_by_album_id(album_id)
            return Response(result("获取相册所有照片成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取相册所有照片失败"), status=400)
