from rest_framework.views import APIView
from rest_framework.response import Response
from apps.comment.service import *
from utils.result import result, throw_error, ERRORCODE
from ..notify.views import NotifyView
from utils.tool import get_current_type_name
from utils.sensitive import filter_sensitive
from apps.notify.service import create_notify

error_code = ERRORCODE['CATEGORY']


class CommentView(APIView):
    """
    评论控制器
    """

    def post(self, request, *args, **kwargs):
        if 'add' in request.path:
            return self.create_comment(request)
        elif 'apply' in request.path:
            return self.apply_comment(request)
        elif 'backGetCommentList' in request.path:
            return self.back_get_comment_list(request)
        elif 'frontGetParentComment' in request.path:
            return self.front_get_parent_comment(request)
        elif 'frontGetChildrenComment' in request.path:
            return self.front_get_children_comment(request)
        elif 'getCommentTotal' in request.path:
            return self.get_comment_total(request)

    def put(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if 'cancelCommentLike' in request.path:
            return self.cancel_comment_like(request, id)
        elif 'thumbUp' in request.path:
            return self.comment_like(request, id)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get('id')
        parent_id = kwargs.get('parent_id')
        if 'delete' in request.path or 'backDelete' in request.path:
            return self.delete_comment(request, id, parent_id)

    def create_comment(self, request):
        """新增评论"""
        try:
            ip = request.META.get("HTTP_X_REAL_IP") or request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get(
                "REMOTE_ADDR")
            request.data['content'] = filter_sensitive(request.data['content'])

            type = request.data.get('type', None)
            for_id = request.data.get('for_id', None)
            author_id = request.data.get('author_id', None)
            from_name = request.data.get('from_name', None)
            from_id = request.data.get('from_id', None)
            content = request.data.get('content', None)
            res = create_comment({**request.data, 'ip': ip.split(":")[-1]})

            if from_id != author_id:
                create_notify({
                    'user_id': author_id,
                    'type': type,
                    'to_id': for_id,
                    'message': f"您的{get_current_type_name(type)}收到了来自于：{from_name} 的评论: {content}！"
                })

            return Response(result("新增评论成功", res), status=201)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "新增评论失败"), status=500)

    def apply_comment(self, request):
        """回复评论"""
        try:
            ip = request.META.get("HTTP_X_REAL_IP") or request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get(
                "REMOTE_ADDR")
            request.data['content'] = filter_sensitive(request.data['content'])

            type = request.data.get('type', None)
            for_id = request.data.get('for_id', None)
            from_name = request.data.get('from_name', None)
            content = request.data.get('content', None)
            from_id = request.data.get('from_id', None)
            to_id = request.data.get('to_id', None)
            res = apply_comment({**request.data, 'ip': ip.split(":")[-1]})

            if from_id != to_id:
                create_notify({
                    'user_id': to_id,
                    'type': type,
                    'to_id': for_id,
                    'message': f"您的收到了来自于：{from_name} 的评论回复: {content}！"
                })

            return Response(result("回复评论成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "回复评论失败"), status=500)

    def comment_like(self, request, comment_id):
        """点赞评论"""
        try:
            res = comment_like(comment_id)
            return Response(result("点赞成功", {'res': res}), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "点赞失败"), status=500)

    def cancel_comment_like(self, request, comment_id):
        """取消点赞评论"""
        try:
            res = cancel_comment_like(comment_id)
            return Response(result("取消点赞成功", {'res': res}), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "取消点赞失败"), status=500)

    def delete_comment(self, request, comment_id, parent_id):
        """删除评论"""
        try:
            res = delete_comment(comment_id, parent_id)
            return Response(result("删除评论成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "删除评论失败"), status=500)

    def back_get_comment_list(self, request):
        """后台条件分页查找评论列表"""
        try:
            current = request.data['current']
            size = request.data['size']
            content = request.data.get('content')
            to_name = request.data.get('to_name')
            from_name = request.data.get('from_name')
            time = request.data.get('time')

            res = back_get_comment_list({
                'current': current,
                'size': size,
                'content': content,
                'to_name': to_name,
                'from_name': from_name,
                'time': time
            })
            return Response(result("分页查找评论成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "分页查找评论失败"), status=500)

    def front_get_parent_comment(self, request):
        """前台条件分页查找父级评论列表"""
        try:
            res = front_get_parent_comment(request)
            return Response(result("分页查找评论成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "分页查找评论失败"), status=500)

    def front_get_children_comment(self, request):
        """前台条件分页查找子级评论列表"""
        try:

            res = front_get_children_comment(request)
            return Response(result("分页查找子评论成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "分页查找子评论失败"), status=500)

    def get_comment_total(self, request):
        """获取当前评论的总条数"""
        try:
            for_id = request.data['for_id']
            type = request.data['type']

            res = get_comment_total(for_id, type)
            return Response(result("获取评论总条数成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取评论总条数失败"), status=500)
