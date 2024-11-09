from rest_framework.views import APIView
from rest_framework.response import Response
from apps.message.service import *
from apps.user.service import get_admin_info
from ..notify.service import create_notify
from utils.result import throw_error, result, ERRORCODE
from utils.sensitive import filter_sensitive
from utils.tool import random_nickname

error_code = ERRORCODE['MESSAGE']


class MessageView(APIView):
    def post(self, request, *args, **kwargs):
        if 'add' in request.path:
            return self.add_message(request)
        elif 'update' in request.path:
            return self.update_message(request)
        elif 'getMessageList' in request.path:
            return self.get_message_list(request)

    def put(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if 'delete' in request.path or 'backDelete' in request.path:
            return self.delete_message(request)
        elif 'like' in request.path:
            return self.message_like(request, id)
        elif 'cancelLike' in request.path:
            return self.cancel_message_like(request, id)

    def get(self, request, *args, **kwargs):
        if 'getAllMessage' in request.path:
            return self.get_all_message(request)
        elif 'getHotTagList' in request.path:
            return self.get_message_tag(request)

    def add_message(self, request):
        try:
            user_id = request.data.get('user_id')
            message = request.data.get('message')
            request.data['nick_name'] = request.data.get('nick_name', random_nickname("游客", 5))
            filtered_message = filter_sensitive(message)
            request.data['message'] = filtered_message
            res = add_message(request.data)
            user_info = get_one_user_info({'id': user_id})
            user_role = user_info.role if user_info else 2

            if user_role != 1:
                admin_users = get_admin_info()
                for admin in admin_users:
                    create_notify({
                        'user_id': admin['id'],
                        'type': 3,
                        'to_id': user_id,
                        'message': f'您收到了来自于：{request.data["nick_name"]} 的留言: {filtered_message}！',
                    })

            return Response(result("发布成功", res), status=201)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "发布失败"), status=500)

    def update_message(self, request):
        try:
            id = request.data.get('id')
            message_data = request.data
            message_data['message'] = filter_sensitive(message_data.get('message', ''))
            res = update_message(id, message_data)
            if res:
                return Response(result("修改成功", res), status=200)
            else:
                return Response(throw_error(error_code, "未找到对应的留言，修改失败"), status=404)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "修改失败"), status=500)

    def delete_message(self, request):
        try:
            id_list = request.data.get('idList', [])
            res = delete_message(id_list)

            return Response(result("删除留言成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "删除留言失败"), status=500)

    def message_like(self, request, id):
        try:
            res = message_like(id)

            return Response(result("留言点赞成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "留言点赞失败"), status=500)

    def cancel_message_like(self, request, id):
        try:
            res = cancel_message_like(id)

            return Response(result("取消留言点赞成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "取消留言点赞失败"), status=500)

    def get_message_list(self, request):
        try:

            res = get_message_list(request)

            return Response(result("分页获取留言成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "分页获取留言失败"), status=500)

    def get_all_message(self, request):
        try:
            res = get_all_message()
            return Response(result("获取留言成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取留言失败"), status=500)

    def get_message_tag(self, request):
        try:
            res = get_message_tag()
            return Response(result("获取留言所有标签成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取留言所有标签失败"),
                            status=500)
