from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.comment.comment import *
from utils.result import result, throw_error, ERRORCODE
from ..notify.views import NotifyView
from utils.tool import get_current_type_name
from utils.sensitive import filter_sensitive

error_code = ERRORCODE['CATEGORY']


class CommentView(APIView):
    """
    评论控制器
    """

    def post(self, request, *args, **kwargs):
        if request.path.endswith('/add/'):
            return self.create_comment(request)
        elif request.path.endswith('/apply/'):
            return self.apply_comment(request)
        elif request.path.endswith('/backGetCommentList/'):
            return self.back_get_comment_list(request)
        elif request.path.endswith('/frontGetParentComment/'):
            return self.front_get_parent_comment(request)
        elif request.path.endswith('/frontGetChildrenComment/'):
            return self.front_get_children_comment(request)
        elif request.path.endswith('/getCommentTotal/'):
            return self.get_comment_total(request)

    def put(self, request, *args, **kwargs):
        if request.path.endswith('/cancelCommentLike/'):
            id = kwargs.get('id')
            return self.cancel_comment_like(request, id)
        elif request.path.endswith('/thumbUp/'):
            id = kwargs.get('id')
            return self.comment_like(request, id)

    def delete(self, request, *args, **kwargs):
        if request.path.endswith('/delete/'):
            id = kwargs.get('id')
            parent_id = kwargs.get('parent_id')
            return self.delete_comment(request, id, parent_id)
        if request.path.endswith('/backDelete/'):
            id = kwargs.get('id')
            parent_id = kwargs.get('parent_id')
            return self.delete_comment(request, id, parent_id)

    def create_comment(self, request):
        """新增评论"""
        try:
            ip = request.META.get("HTTP_X_REAL_IP") or request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get(
                "REMOTE_ADDR")
            request.data['content'] = filter_sensitive(request.data['content'])

            res = create_comment({**request.data, 'ip': ip.split(":")[-1]})
            type = request.data['type']
            for_id = request.data['for_id']
            author_id = request.data['author_id']
            from_name = request.data['from_name']
            from_id = request.data['from_id']
            content = request.data['content']

            if from_id != author_id:
                NotifyView.add_notify({
                    'user_id': author_id,
                    'type': type,
                    'to_id': for_id,
                    'message': f"您的{get_current_type_name(type)}收到了来自于：{from_name} 的评论: {content}！"
                })

            return Response(result("新增评论成功", {'res': res}), status=status.HTTP_201_CREATED)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "新增评论失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def apply_comment(self, request):
        """回复评论"""
        try:
            ip = request.META.get("HTTP_X_REAL_IP") or request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get(
                "REMOTE_ADDR")
            request.data['content'] = filter_sensitive(request.data['content'])

            res = apply_comment({**request.data, 'ip': ip.split(":")[-1]})
            type = request.data['type']
            for_id = request.data['for_id']
            from_name = request.data['from_name']
            content = request.data['content']
            from_id = request.data['from_id']
            to_id = request.data['to_id']

            if from_id != to_id:
                NotifyView.add_notify({
                    'user_id': to_id,
                    'type': type,
                    'to_id': for_id,
                    'message': f"您的收到了来自于：{from_name} 的评论回复: {content}！"
                })

            return Response(result("回复评论成功", {'res': res}), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "回复评论失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def comment_like(self, request, comment_id):
        """点赞评论"""
        try:
            res = comment_like(comment_id)
            return Response(result("点赞成功", {'res': res}), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "点赞失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def cancel_comment_like(self, request, comment_id):
        """取消点赞评论"""
        try:
            res = cancel_comment_like(comment_id)
            return Response(result("取消点赞成功", {'res': res}), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "取消点赞失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_comment(self, request, comment_id, parent_id):
        """删除评论"""
        try:
            res = delete_comment(comment_id, parent_id)
            return Response(result("删除评论成功", {'res': res}), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "删除评论失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            return Response(result("分页查找评论成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "分页查找评论失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def front_get_parent_comment(self, request):
        """前台条件分页查找父级评论列表"""
        try:
            ip = request.META.get("HTTP_X_REAL_IP") or request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get(
                "REMOTE_ADDR")
            ip = ip.split(":")[-1]
            current = request.data['current']
            size = request.data['size']
            type = request.data['type']
            for_id = request.data['for_id']
            user_id = request.data['user_id']
            order = request.data['order']

            res = front_get_parent_comment({
                'current': current,
                'size': size,
                'type': type,
                'for_id': for_id,
                'user_id': user_id,
                'order': order,
                'ip': ip
            })
            return Response(result("分页查找评论成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "分页查找评论失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def front_get_children_comment(self, request):
        """前台条件分页查找子级评论列表"""
        try:
            ip = request.META.get("HTTP_X_REAL_IP") or request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get(
                "REMOTE_ADDR")
            ip = ip.split(":")[-1]
            current = request.data['current']
            size = request.data['size']
            type = request.data['type']
            for_id = request.data['for_id']
            user_id = request.data['user_id']
            parent_id = request.data['parent_id']

            res = front_get_children_comment({
                'current': current,
                'size': size,
                'type': type,
                'for_id': for_id,
                'user_id': user_id,
                'parent_id': parent_id,
                'ip': ip
            })
            return Response(result("分页查找子评论成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "分页查找子评论失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_comment_total(self, request):
        """获取当前评论的总条数"""
        try:
            for_id = request.data['for_id']
            type = request.data['type']

            res = get_comment_total({'for_id': for_id, 'type': type})
            return Response(result("获取评论总条数成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取评论总条数失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
