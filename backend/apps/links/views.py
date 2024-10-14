from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.links.service import *
from ..notify.views import NotifyView
from utils.result import throw_error, result, ERRORCODE

error_code = ERRORCODE['LINKS']


class LinksView(APIView):
    def post(self, request, *args, **kwargs):
        if 'add' in request.path or 'backUpdate' in request.path:
            return self.add_or_update_links(request)
        elif 'frontUpdate' in request.path:
            return self.front_update_links(request)
        elif 'getLinksList' in request.path:
            return self.get_links_list(request)

    def put(self, request, *args, **kwargs):
        if 'delete' in request.path:
            return self.delete_links(request)
        elif 'approve' in request.path:
            return self.approve_links(request)

    def add_or_update_links(self, request):
        try:
            id_ = request.data.get('id')
            site_name = request.data.get('site_name')
            res = add_or_update_links(request.data)

            if not id_:
                NotifyView.add_notify({
                    'user_id': 1,
                    'type': 4,  # 友链
                    'message': f'您的收到了来自于：{site_name} 的友链申请，点我去后台审核！',
                })

            msg = "修改" if id_ else "发布"
            return Response(result(f"{msg}友链成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, f"{msg}友链失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def front_update_links(self, request):
        try:
            site_name = request.data.get('site_name')
            res = add_or_update_links(request.data)

            NotifyView.add_notify({
                'user_id': 1,
                'type': 4,  # 友链
                'message': f'您的收到了来自于：{site_name} 的友链修改申请，点我去后台审核！',
            })

            return Response(result("修改友链成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "修改友链失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_links(self, request):
        try:
            id_list = request.data.get('idList')
            res = delete_links(id_list)
            return Response(result("删除友链成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "删除友链失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def approve_links(self, request):
        try:
            id_list = request.data.get('idList')
            res = approve_links(id_list)
            return Response(result("审核友链成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "审核友链失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_links_list(self, request):
        try:
            current = request.data.get('current')
            size = request.data.get('size')
            time = request.data.get('time')
            status_ = request.data.get('status')
            site_name = request.data.get('site_name')
            res = get_links_list(current, size, time, status_, site_name)

            return Response(result("查询友链成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "查询友链失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
