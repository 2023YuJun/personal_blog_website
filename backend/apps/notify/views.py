from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.notify.notify import *
from utils.result import result, ERRORCODE, throw_error

error_code = ERRORCODE['NOTIFY']


class NotifyView(APIView):
    def post(self, request, *args, **kwargs):
        if request.path.endswith('/getNotifyList/'):
            return self.get_notify_list(request)

    def put(self, request, *args, **kwargs):
        if request.path.endswith('/update/'):
            id = kwargs.get('id')
            return self.update_notify(request, id)
        elif request.path.endswith('/delete/'):
            id = kwargs.get('id')
            return self.delete_notifys(request, id)

    def add_notify(self, request):
        try:
            user_id = request.data['user_id']
            notify_type = request.data['type']
            to_id = request.data['to_id']
            message = request.data['message']
            create_notify(
                {'user_id': user_id, 'type': notify_type, 'to_id': to_id, 'message': message})
            return Response(result("新增消息通知成功"), status=status.HTTP_201_CREATED)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "新增消息通知失败"), status=status.HTTP_400_BAD_REQUEST)

    def update_notify(self, request, id):
        try:
            res = update_notify(id)
            return Response(result("已阅消息通知成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "已阅消息通知失败"), status=status.HTTP_400_BAD_REQUEST)

    def delete_notifys(self, request, id):
        try:
            res = delete_notifys(id)
            return Response(result("删除消息通知成功", {'res': res}), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "删除消息通知失败"), status=status.HTTP_400_BAD_REQUEST)

    def get_notify_list(self, request):
        try:
            current = request.data['current']
            size = request.data['size']
            user_id = request.data['userId']
            res = get_notify_list({'current': current, 'size': size, 'userId': user_id})
            return Response(result("分页查找消息通知成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "分页查询消息通知失败"), status=status.HTTP_400_BAD_REQUEST)
