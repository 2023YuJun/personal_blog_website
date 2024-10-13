from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.message.message import *
from ..notify.views import NotifyView
from utils.result import throw_error, result, ERRORCODE
from utils.sensitive import filter_sensitive
from utils.tool import random_nickname

error_code = ERRORCODE['MESSAGE']


class MessageView(APIView):
    def post(self, request, *args, **kwargs):
        if request.path.endswith('/add/'):
            return self.add_message(request)
        elif request.path.endswith('/update/'):
            return self.update_message(request)
        elif request.path.endswith('/getMessageList/'):
            return self.get_message_list(request)

    def put(self, request, *args, **kwargs):
        if request.path.endswith('/delete/'):
            return self.delete_message(request)
        elif request.path.endswith('/backDelete/'):
            return self.delete_message(request)
        elif request.path.endswith('/like/'):
            id = kwargs.get('id')
            return self.message_like(request, id)
        elif request.path.endswith('/cancelLike/'):
            id = kwargs.get('id')
            return self.cancel_message_like(request, id)

    def get(self, request, *args, **kwargs):
        if request.path.endswith('/getAllMessage/'):
            return self.get_all_message(request)
        elif request.path.endswith('/getHotTagList/'):
            return self.get_message_tag(request)

    def add_message(self, request):
        try:
            user_id = request.data.get('user_id')
            message = request.data.get('message')
            nick_name = request.data.get('nick_name', random_nickname("游客", 5))

            message = filter_sensitive(message)
            res = add_message({
                'nick_name': nick_name,
                'user_id': user_id,
                'message': message,
            })

            if user_id != 1:
                NotifyView.add_notify({
                    'user_id': 1,
                    'type': 3,
                    'message': f'您收到了来自于：{nick_name} 的留言: {message}！',
                })

            return Response(result("发布成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "发布失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_message(self, request):
        try:
            message = request.data.get('message')
            message = filter_sensitive(message)
            id = request.data.get('id')
            res = update_message(id, message)

            return Response(result("修改成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "修改失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_message(self, request):
        try:
            id_list = request.data.get('idList')
            res = delete_message(id_list)

            return Response(result("删除留言成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "删除留言失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def message_like(self, request, id):
        try:
            res = message_like(id)

            return Response(result("留言点赞成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "留言点赞失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def cancel_message_like(self, request, id):
        try:
            res = cancel_message_like(id)

            return Response(result("取消留言点赞成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "取消留言点赞失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_message_list(self, request):
        try:

            res = get_message_list(request)

            return Response(result("分页获取留言成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "分页获取留言失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_all_message(self, request):
        try:
            res = get_all_message()
            return Response(result("获取留言成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取留言失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_message_tag(self, request):
        try:
            res = get_message_tag()
            return Response(result("获取留言所有标签成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取留言所有标签失败"),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
