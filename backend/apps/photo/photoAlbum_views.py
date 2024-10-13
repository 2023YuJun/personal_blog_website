from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.photo.photoAlbum import *
from utils.result import result, ERRORCODE, throw_error
from utils.minioUpload import delete_minio_imgs

error_code = ERRORCODE['PHOTOALBUM']


class PhotoAlbunView(APIView):
    def post(self, request, *args, **kwargs):
        if request.path.endswith('/add/'):
            return self.add_album(request)
        elif request.path.endswith('/photoAlbum/'):
            return self.get_album_list(request)

    def put(self, request, *args, **kwargs):
        if request.path.endswith('/update/'):
            return self.update_album(request)

    def get(self, request, *args, **kwargs):
        if request.path.endswith('/getAllAlbumList/'):
            return self.get_all_album_list(request)

    def delete(self, request, *args, **kwargs):
        if request.path.endswith('/delete/'):
            id = kwargs.get('id')
            return self.delete_album(id)

    def add_album(self, request):
        try:
            album_name = request.data.get('album_name')
            one = get_one_album({'album_name': album_name})
            if one:
                return Response(throw_error(error_code, "已经存在相同的相册名称，换一个试试"),
                                status=status.HTTP_400_BAD_REQUEST)
            album_cover = request.data.get('album_cover')
            description = request.data.get('description')
            res = add_album(album_name, album_cover, description)
            return Response(result("创建相册成功", res), status=status.HTTP_201_CREATED)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "创建相册失败"), status=status.HTTP_400_BAD_REQUEST)

    def delete_album(self, id):
        try:
            one = get_one_album({'id': id})
            album_cover_key = one.album_cover.split("/").pop()
            delete_minio_imgs([album_cover_key])

            res = delete_album(id)
            return Response(result("删除相册成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "删除相册失败"), status=status.HTTP_400_BAD_REQUEST)

    def update_album(self, request):
        try:
            id = request.data['id']
            album_name = request.data['album_name']
            album_cover = request.data.get('album_cover')
            description = request.data.get('description')
            one = get_one_album({'album_name': album_name})
            if one and one.id != id:
                return Response(throw_error(error_code, "已经存在相同的相册名称，换一个试试"),
                                status=status.HTTP_400_BAD_REQUEST)

            album = get_one_album({'id': id})

            # 删除原来存储的照片
            if album_cover != album.album_cover:
                album_cover_key = album.album_cover.split("/").pop()
                delete_minio_imgs([album_cover_key])

            res = update_album(id, album_name, album_cover, description)
            return Response(result("修改相册成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "修改相册失败"), status=status.HTTP_400_BAD_REQUEST)

    def get_album_list(self, request):
        try:
            current = request.data.get('current')
            size = request.data.get('size')
            album_name = request.data.get('album_name')
            res = get_album_list(current,  size, album_name)
            return Response(result("获取相册列表成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取相册列表失败"), status=status.HTTP_400_BAD_REQUEST)

    def get_all_album_list(self, request):
        try:
            res = get_all_album_list()
            return Response(result("获取所有相册列表成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取所有相册列表失败"), status=status.HTTP_400_BAD_REQUEST)
