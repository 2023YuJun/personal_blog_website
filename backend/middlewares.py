import jwt
from django.core.cache import cache
from django.conf import settings
from django.http import JsonResponse
from utils.result import ERRORCODE, throw_error
from django.utils import timezone
from datetime import timedelta
error_code = ERRORCODE['AUTH']  # 用户权限不足
token_error_code = ERRORCODE['AUTHTOKEN']  # 用户登录过期


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 只对特定路径应用中间件
        if request.path in [
            'article/add/',
            'article/update/',
            'article/updateTop/',
            'article/delete/',
            'article/revert/',
            'article/isPublic/',
            'article/getArticleList/',
            'chat/delete/',
            'comment/delete/',
            'comment/backDelete/',
            'config/update/',
            'pageHeader/addOrUpdate/',
            'pageHeader/delete/',
            'links/backUpdate/',
            'links/delete/',
            'links/approve/',
            'message/backDelete/',
            'photo/add/',
            'photo/delete/',
            'photo/revert/',
            'photoAlbum/add/',
            'photoAlbum/delete/',
            'photoAlbum/update/',
            'tag/add/',
            'tag/update/',
            'tag/delete/',
            'talk/publishTalk/',
            'talk/updateTalk/',
            'talk/deleteTalkById/',
            'talk/togglePublic/',
            'talk/toggleTop/',
            'talk/revertTalk/',
            'user/updateOwnUserInfo/',
            'user/updatePassword/',
            'user/updateRole/',
            'user/adminUpdateUserInfo/',
            'user/getUserList/',
        ]:
            authorization = request.headers.get('Authorization')
            if not authorization:
                print("您没有权限访问，请先登录")
                return JsonResponse(throw_error(token_error_code, "您没有权限访问，请先登录"), status=403)
            token = authorization.replace("Bearer ", "")

            try:
                user = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS2106"])
                request.user = user  # 将用户信息保存到请求中
            except jwt.ExpiredSignatureError:
                print("token已过期")
                return JsonResponse(throw_error(token_error_code, "token已过期"), status=401)
            except jwt.InvalidTokenError:
                print("无效的token")
                return JsonResponse(throw_error(error_code, "无效的token"), status=401)
        response = self.get_response(request)
        return response


class NeedAdminAuthNotNeedSuperMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in [
            'article/add/',
            'article/update/',
            'article/updateTop/',
            'article/delete/',
            'article/revert/',
            'article/isPublic/',
            'comment/delete/',
            'links/backUpdate/',
            'links/delete/',
            'links/approve/',
            'message/backDelete/',
            'photo/add/',
            'photo/delete/',
            'photo/revert/',
            'photoAlbum/add/',
            'photoAlbum/delete/',
            'photoAlbum/update/',
            'tag/add/',
            'tag/update/',
            'tag/delete/',
            'talk/publishTalk/',
            'talk/updateTalk/',
            'talk/deleteTalkById/',
            'talk/togglePublic/',
            'talk/toggleTop/',
            'talk/revertTalk/',
            'user/updateRole/',
            'user/adminUpdateUserInfo/',
        ]:
            authorization = request.headers.get('Authorization')
            if not authorization:
                print("您没有权限访问，请先登录")
                return JsonResponse(throw_error(token_error_code, "您没有权限访问，请先登录"), status=403)
            token = authorization.replace("Bearer ", "")
            try:
                user = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS2106"])
                role = user['role']
                username = user['username']

                if role != 1:
                    return JsonResponse(throw_error(error_code, "普通用户仅限查看"), status=403)
                if username == "admin":
                    return JsonResponse(
                        throw_error(error_code, "admin是配置的用户，没有用户信息，建议注册账号再发布博客内容"),
                        status=403)
            except jwt.ExpiredSignatureError:
                print("token已过期")
                return JsonResponse(throw_error(token_error_code, "token已过期"), status=401)
            except jwt.InvalidTokenError:
                print("无效的token")
                return JsonResponse(throw_error(error_code, "无效的token"), status=401)
        response = self.get_response(request)
        return response


class AdminAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in [
            'chat/delete/',
            'config/update/',
            'pageHeader/addOrUpdate/',
            'pageHeader/delete/',
        ]:
            authorization = request.headers.get('Authorization')
            if not authorization:
                print("您没有权限访问，请先登录")
                return JsonResponse(throw_error(token_error_code, "您没有权限访问，请先登录"), status=403)
            token = authorization.replace("Bearer ", "")

            try:
                user = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS2106"])
                if user['role'] != 1:
                    return JsonResponse(throw_error(error_code, "普通用户仅限查看"), status=403)
            except jwt.ExpiredSignatureError:
                print("token已过期")
                return JsonResponse(throw_error(token_error_code, "token已过期"), status=401)
            except jwt.InvalidTokenError:
                print("无效的token")
                return JsonResponse(throw_error(error_code, "无效的token"), status=401)

        response = self.get_response(request)
        return response


class SuperAdminAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in [
            'user/updateOwnUserInfo/',
            'user/updatePassword/',
        ]:
            authorization = request.headers.get('Authorization')
            if not authorization:
                print("您没有权限访问，请先登录")
                return JsonResponse(throw_error(token_error_code, "您没有权限访问，请先登录"), status=403)
            token = authorization.replace("Bearer ", "")

            try:
                user = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS2106"])
                if user['username'] == 'admin':
                    return JsonResponse({"message": "管理员信息只可通过配置信息修改"}, status=403)
            except jwt.ExpiredSignatureError:
                print("token已过期")
                return JsonResponse(throw_error(token_error_code, "token已过期"), status=401)
            except jwt.InvalidTokenError:
                print("无效的token")
                return JsonResponse(throw_error(error_code, "无效的token"), status=401)

        response = self.get_response(request)
        return response


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 获取请求路径
        path = request.path

        # 根据路径设置不同的请求限制参数
        limits = {
            'article/like/': {'max_requests': 10, 'interval': 10, 'message': '文章点赞过于频繁 请稍后再试'},
            'article/cancelLike/': {'max_requests': 10, 'interval': 10, 'message': '取消文章点赞过于频繁 请稍后再试'},
            'comment/add/': {'max_requests': 20, 'interval': 10, 'message': '评论过于频繁 请稍后再试'},
            'comment/apply/': {'max_requests': 20, 'interval': 10, 'message': '回复评论过于频繁 请稍后再试'},
            'comment/thumbUp/': {'max_requests': 10, 'interval': 10, 'message': '点赞过于频繁 请稍后再试'},
            'comment/cancelCommentLike/': {'max_requests': 10, 'interval': 10, 'message': '取消点赞过于频繁 请稍后再试'},
            'upload/img/': {'max_requests': 100, 'interval': 10, 'message': '上传图片过于频繁 请稍后再试'},
            'config/addView/': {'max_requests': 100, 'interval': 10, 'message': '访问网站过于频繁 请稍后再试'},
            'like/addLike/': {'max_requests': 10, 'interval': 10, 'message': '点赞过于频繁 请稍后再试'},
            'like/cancelLike/': {'max_requests': 10, 'interval': 10, 'message': '取消点赞过于频繁 请稍后再试'},
            'links/add/': {'max_requests': 10, 'interval': 10, 'message': '新增过于频繁 请稍后再试'},
            'message/add/': {'max_requests': 10, 'interval': 10, 'message': '留言过于频繁 请稍后再试'},
            'message/update/': {'max_requests': 10, 'interval': 10, 'message': '修改留言过于频繁 请稍后再试'},
            'message/delete/': {'max_requests': 10, 'interval': 10, 'message': '删除过于频繁 请稍后再试'},
            'message/like/': {'max_requests': 10, 'interval': 10, 'message': '留言点赞过于频繁 请稍后再试'},
            'message/cancelLike/': {'max_requests': 10, 'interval': 10, 'message': '留言点赞过于频繁 请稍后再试'},
            'talk/like/': {'max_requests': 10, 'interval': 10, 'message': '说说点赞过于频繁 请稍后再试'},
            'talk/cancelLike/': {'max_requests': 10, 'interval': 10, 'message': '说说取消点赞过于频繁 请稍后再试'},
            'user/register/': {'max_requests': 3, 'interval': 10, 'message': '用户注册过于频繁 请稍后再试'},
        }

        limit = limits.get(path)
        if limit:
            ip = self.get_client_ip(request)
            key = f"rate_limit_{ip}_{path}"
            current_time = timezone.localtime()
            # 从缓存中获取请求数据
            request_data = cache.get(key, {'count': 0, 'first_request_time': current_time})
            # 计算时间差，使用 Django 的 timedelta
            time_since_first_request = current_time - request_data['first_request_time']
            if time_since_first_request < timedelta(seconds=limit['interval']):
                # 如果在时间窗口内，且请求数超过限制，返回 429 错误
                if request_data['count'] >= limit['max_requests']:
                    return JsonResponse({"message": limit['message']}, status=429)
                else:
                    # 否则增加请求计数
                    request_data['count'] += 1
            else:
                # 如果超过了时间窗口，重置计数和首次请求时间
                request_data = {'count': 1, 'first_request_time': current_time}
                # 更新缓存，并设置过期时间为剩余时间窗口
            cache.set(key, request_data, timeout=limit['interval'])

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """获取客户端 IP 地址"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
