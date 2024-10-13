from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from utils.result import result, ERRORCODE, throw_error
from apps.talk.talk import *

error_code = ERRORCODE['TALK']


class TalkView(APIView):
    """
    说说控制器
    """

    def post(self, request, *args, **kwargs):
        if request.path.endswith('/publishTalk/'):
            return self.publish_talk(request)
        elif request.path.endswith('/getTalkList/'):
            return self.get_talk_list(request)
        elif request.path.endswith('/blogGetTalkList/'):
            return self.blog_get_talk_list(request)

    def put(self, request, *args, **kwargs):
        if request.path.endswith('/updateTalk/'):
            return self.update_talk(request)
        elif request.path.endswith('/togglePublic/'):
            id = kwargs.get('id')
            status = kwargs.get('status')
            return self.toggle_public(request, id, status)
        elif request.path.endswith('/toggleTop/'):
            id = kwargs.get('id')
            is_top = kwargs.get('is_top')
            return self.toggle_top(request, id, is_top)
        elif request.path.endswith('/revertTalk/'):
            id = kwargs.get('id')
            return self.revert_talk(request, id)
        elif request.path.endswith('/like/'):
            id = kwargs.get('id')
            return self.talk_like(request, id)
        elif request.path.endswith('/cancelLike/'):
            id = kwargs.get('id')
            return self.cancel_talk_like(request, id)

    def get(self, request, *args, **kwargs):
        if request.path.endswith('/getTalkById/'):
            id = kwargs.get('id')
            return self.get_talk_by_id(request, id)

    def delete(self, request, *args, **kwargs):
        if request.path.endswith('/deleteTalkById/'):
            id = kwargs.get('id')
            status = kwargs.get('status')
            return self.delete_talk_by_id(request, id, status)

    def publish_talk(self, request):
        """发布说说"""
        try:
            res = publish_talk(request.data)
            return Response(result("发布说说成功", {"id": res.id}), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "发布说说失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_talk(self, request):
        """修改说说"""
        try:
            res = update_talk(request.data)
            return Response(result("修改说说成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "修改说说失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_talk_by_id(self, request, id, status):
        """删除说说"""
        message = "删除" if int(status) == 3 else "回收"
        try:
            res = delete_talk_by_id(id, status)
            return Response(result(f"{message}说说成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, f"{message}说说失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def toggle_public(self, request, id, status):
        """公开/私密说说"""
        message = "公开" if int(status) == 1 else "私密"
        try:
            res = toggle_public(id, status)
            return Response(result(f"{message}说说成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, f"{message}说说失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def talk_like(self, request, id):
        """说说点赞"""
        try:
            res = talk_like(id)
            return Response(result("点赞成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "点赞失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def cancel_talk_like(self, request, id):
        """取消说说点赞"""
        try:
            res = cancel_talk_like(id)
            return Response(result("取消点赞成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "取消点赞失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def revert_talk(self, request, id):
        """恢复说说"""
        try:
            res = revert_talk(id)
            return Response(result("恢复说说成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "恢复说说失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def toggle_top(self, request, id, is_top):
        """切花置顶状态"""
        message = "置顶" if int(is_top) == 1 else "取消置顶"
        try:
            res = toggle_top(id, is_top)
            return Response(result(f"{message}说说成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, f"{message}说说失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_talk_list(self, request):
        """分页获取说说"""
        try:
            current = request.data.get('current')
            size = request.data.get('size')
            status = request.data.get('status')
            res = get_talk_list(current, size, status)
            return Response(result("获取说说列表成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取说说列表失败"), status=500)

    def get_talk_by_id(self, request, id):
        """根据id获取说说详情"""
        try:
            res = get_talk_by_id(id)
            return Response(result("获取说说详情成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取说说详情失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def blog_get_talk_list(self, request):
        """前台获取说说列表"""
        try:
            current = request.data.get('current')
            size = request.data.get('size')
            user_id = request.data.get('user_id')
            ip = request.META.get("HTTP_X_REAL_IP") or request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get(
                "REMOTE_ADDR")
            ip = ip.split(":")[-1]
            res = blog_get_talk_list(current, size, user_id, ip)
            return Response(result("获取说说列表成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取说说列表失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
