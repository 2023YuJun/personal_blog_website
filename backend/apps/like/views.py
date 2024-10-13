from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.like.like import *
from apps.article.article_service import article_like, cancel_article_like
from apps.talk.talk import talk_like, cancel_talk_like
from apps.comment.comment import comment_like, cancel_comment_like
from apps.message.message import message_like, cancel_message_like
from utils.result import throw_error, result, ERRORCODE

error_code = ERRORCODE['LIKE']


class LikeView(APIView):
    def post(self, request, *args, **kwargs):
        if request.path.endswith('/addLike/'):
            return self.add_like(request)
        elif request.path.endswith('/cancelLike/'):
            return self.cancel_like(request)
        elif request.path.endswith('/getIsLikeByIdOrIpAndType/'):
            return self.get_is_like_by_id_and_type(request)

    def add_like(self, request):
        try:
            ip = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get(
                'REMOTE_ADDR')
            ip = ip.split(':')[-1]  # 获取最后一部分
            for_id = request.data.get('for_id')
            type_ = request.data.get('type')
            user_id = request.data.get('user_id')

            if not for_id:
                return Response(throw_error(error_code, "点赞对象不能为空"), status=status.HTTP_400_BAD_REQUEST)
            if not type_:
                return Response(throw_error(error_code, "点赞类型不能为空"), status=status.HTTP_400_BAD_REQUEST)

            if not user_id:
                is_like = get_is_like_by_ip_and_type(for_id, type_, ip)
                if is_like:
                    return Response(throw_error(error_code, "您已经点过赞了"), status=status.HTTP_400_BAD_REQUEST)
                res = add_like({'for_id': for_id, 'type': type_, 'ip': ip})
            else:
                is_like = get_is_like_by_id_and_type(for_id, type_, user_id)
                if is_like:
                    return Response(throw_error(error_code, "您已经点过赞了"), status=status.HTTP_400_BAD_REQUEST)
                res = add_like({'for_id': for_id, 'type': type_, 'user_id': user_id})

            if not res:
                return Response(throw_error(error_code, "点赞失败"), status=status.HTTP_400_BAD_REQUEST)

            # 点赞类型 1 文章 2 说说 3 留言 4 评论
            if type_ == "1":
                article_like(for_id)
            elif type_ == "2":
                talk_like(for_id)
            elif type_ == "3":
                message_like(for_id)
            elif type_ == "4":
                comment_like(for_id)

            return Response(result("点赞成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "点赞失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def cancel_like(self, request):
        try:
            for_id = request.data.get('for_id')
            type_ = request.data.get('type')
            user_id = request.data.get('user_id')
            ip = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get(
                'REMOTE_ADDR')
            ip = ip.split(':')[-1]

            if not for_id:
                return Response(throw_error(error_code, "取消点赞对象不能为空"), status=status.HTTP_400_BAD_REQUEST)
            if not type_:
                return Response(throw_error(error_code, "取消点赞类型不能为空"), status=status.HTTP_400_BAD_REQUEST)

            if not user_id:
                is_like = get_is_like_by_ip_and_type(for_id, type_, ip)
                if not is_like:
                    return Response(throw_error(error_code, "您没有点过赞"), status=status.HTTP_400_BAD_REQUEST)
                res = cancel_like(for_id, type_, ip)
            else:
                is_like = get_is_like_by_id_and_type(for_id, type_, user_id)
                if not is_like:
                    return Response(throw_error(error_code, "您没有点过赞"), status=status.HTTP_400_BAD_REQUEST)
                res = cancel_like(for_id, type_, user_id)

            if not res:
                return Response(throw_error(error_code, "取消点赞失败"), status=status.HTTP_400_BAD_REQUEST)

            if type_ == "1":
                cancel_article_like(for_id)
            elif type_ == "2":
                cancel_talk_like(for_id)
            elif type_ == "3":
                cancel_message_like(for_id)
            elif type_ == "4":
                cancel_comment_like(for_id)

            return Response(result("取消点赞成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "取消点赞失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_is_like_by_id_and_type(self, request):
        try:
            for_id = request.data.get('for_id')
            type_ = request.data.get('type')
            user_id = request.data.get('user_id')
            ip = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get(
                'REMOTE_ADDR')
            ip = ip.split(':')[-1]

            if not for_id:
                return Response(throw_error(error_code, "取消点赞对象不能为空"), status=status.HTTP_400_BAD_REQUEST)
            if not type_:
                return Response(throw_error(error_code, "取消点赞类型不能为空"), status=status.HTTP_400_BAD_REQUEST)

            if not user_id:
                res = get_is_like_by_ip_and_type(for_id, type_, ip)
            else:
                res = get_is_like_by_id_and_type(for_id,type_,user_id)

            return Response(result("获取用户是否点赞成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取用户是否点赞失败"),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
