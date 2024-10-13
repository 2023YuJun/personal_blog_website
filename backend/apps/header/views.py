from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from utils.result import result, ERRORCODE, throw_error
from apps.header.header import *
from utils.minioUpload import delete_minio_imgs

error_code = ERRORCODE['HEADER']


class HeaderView(APIView):
    """
    背景图控制器
    """

    def post(self, request, *args, **kwargs):
        if request.path.endswith('/addOrUpdate/'):
            return self.add_or_update_header(request)
        elif request.path.endswith('/delete/'):
            return self.delete_header(request)

    def get(self, request, *args, **kwargs):
        if request.path.endswith('/getAll/'):
            return self.get_all_header(request)

    def add_or_update_header(self, request):
        """新增/修改背景图"""
        try:
            id = request.data.get('id')
            route_name = request.data.get('route_name')

            if not id:
                flag = get_one_by_path(route_name)
                if flag:
                    return Response(throw_error(error_code, "已经存在相同的背景路径"),
                                    status=status.HTTP_400_BAD_REQUEST)

            if id:
                flag = get_one_by_path(route_name)
                if flag and flag.id != id:
                    return Response(throw_error(error_code, "已经存在相同的背景路径"),
                                    status=status.HTTP_400_BAD_REQUEST)

            msg = "修改" if id else "新增"
            res = add_or_update_header(request.data)
            return Response(result(f"{msg}背景成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, f"{msg}背景失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_header(self, request):
        """删除背景图"""
        try:
            id = request.data.get('id')
            url = request.data.get('url')
            res = delete_header(id)

            if url:
                # 远程删除图片
                arr = [url.split("/")[-1]]
                delete_minio_imgs(arr)

            return Response(result("删除背景成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "删除背景失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_all_header(self, request):
        """获取所有背景图"""
        try:
            res = get_all_headers()
            return Response(result("获取所有背景成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取所有背景失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
