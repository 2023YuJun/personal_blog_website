import jwt
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.result import result
from django.conf import settings
from apps.user.service import *
from utils.tool import get_ip_address
from utils.minioUpload import delete_minio_imgs

error_code = ERRORCODE['USER']


class UserView(APIView):
    """用户控制器"""

    def post(self, request, *args, **kwargs):
        if request.path.endswith('/register/'):
            return self.register(request)
        elif request.path.endswith('/login/'):
            return self.login(request)
        elif request.path.endswith('/getUserList/'):
            return self.get_user_list(request)

    def put(self, request, *args, **kwargs):
        if request.path.endswith('/updateOwnUserInfo/'):
            return self.update_own_user_info(request)
        elif request.path.endswith('/updatePassword/'):
            return self.update_password(request)
        elif request.path.endswith('/updateRole/'):
            id = kwargs.get('id')
            role = kwargs.get('role')
            return self.update_role(request, id, role)
        elif request.path.endswith('/adminUpdateUserInfo/'):
            return self.admin_update_user_info(request)

    def get(self, request, *args, **kwargs):
        if request.path.endswith('/getUserInfoById/'):
            id = kwargs.get('id')
            return self.get_user_info(request, id)

    def register(self, request):
        """用户注册"""
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            validate_username_password(username, password)
            verify_user(username)
            res = create_user(request.data)
            ip = request.META.get("HTTP_X_REAL_IP") or request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get(
                "REMOTE_ADDR")
            update_ip(res.id, ip.split(":")[-1])
            return Response(result("用户注册成功", {"id": res.id, "username": res.username}))
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "用户注册失败"), status=500)

    def login(self, request):
        """登录"""
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            validate_username_password(username, password)
            verify_login_credentials(username, password)
            if username == "admin":
                if password == settings.ADMIN_PASSWORD:
                    token = jwt.encode({"nick_name": "超级管理员", "id": 5201314, "role": 1, "username": "admin"},
                                       settings.JWT_SECRET, algorithm="HS256")
                    return JsonResponse(result("超级管理员登录成功",
                                               {"token": token, "username": "超级管理员", "role": 1, "id": 5201314}))
                else:
                    return JsonResponse(throw_error(error_code, "密码错误"), status=400)
            else:
                res = get_one_user_info({"username": username})
                ip = request.META.get("HTTP_X_REAL_IP") or request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get(
                    "REMOTE_ADDR")
                update_ip(res.id, ip.split(":")[-1])
                ip_address = get_ip_address()
                payload = {
                    "id": res.id,
                    "username": res.username,
                    "role": res.role,
                    "nick_name": res.nick_name
                }
                token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
                return JsonResponse(result("用户登录成功",
                                           {"token": token, "username": res.username, "role": res.role, "id": res.id,
                                            "ipAddress": ip_address}))

        except Exception as err:
            print(err)
            return JsonResponse(throw_error(error_code, "用户登陆失败"), status=500)

    def update_own_user_info(self, request):
        """用户修改自己的用户信息"""
        try:
            user_id = request.user.id
            avatar = request.data.get("avatar")
            one = get_one_user_info({"id": user_id})

            # 服务器删除原来的头像
            if one.avatar and one.avatar != avatar:
                delete_minio_imgs([one.avatar.split("/")[-1]])

            res = update_own_user_info(user_id, request.data)
            return Response(result("修改用户成功", res))
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "修改用户失败"), status=500)

    def update_password(self, request):
        """修改密码"""
        try:
            username = request.data.get("username")
            current_password = request.data.get("current_password")
            password1 = request.data.get("password1")
            password2 = request.data.get("password2")
            user_id = request.user.id

            if user_id == 2:
                return Response(throw_error(error_code, "测试用户密码不可以修改哦"), status=400)

            verify_update_password(username, current_password, password1, password2)
            res = update_password(user_id, password1)
            return Response(result("修改用户密码成功", res))
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "修改用户密码失败"), status=500)

    def update_role(self, request, id, role):
        """修改用户角色"""
        try:
            res = update_role(id, role)
            return Response(result("修改角色成功", res))
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "修改角色失败"), status=500)

    def get_user_list(self, request):
        """分页获取用户列表"""
        try:
            res = get_user_list(request)
            return Response(result("分页获取用户列表成功", res))
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "分页获取用户列表失败"), status=500)

    def get_user_info(self, request, id):
        """根据用户id获取当前登录人信息"""
        try:
            if id == 5201314:
                return Response(result("获取用户信息成功", {"id": 5201314, "role": 1, "nick_name": "超级管理员"}))
            else:
                res = get_one_user_info({"id": id})
                ip_address = get_ip_address()
                res_info = {key: value for key, value in res.items() if key not in ["password", "username", "ip"]}
                res_info["ipAddress"] = ip_address
                return Response(result("获取用户信息成功", res_info))
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取用户信息失败"), status=500)

    def admin_update_user_info(self, request):
        """管理员根据用户id修改用户的信息"""
        try:
            user_id = request.data.get("id")
            avatar = request.data.get("avatar")
            one = get_one_user_info({"id": user_id})

            # 服务器删除原来的头像
            if one.avatar and one.avatar != avatar:
                delete_minio_imgs([one.avatar.split("/")[-1]])

            res = admin_update_user_info(request.data)
            return Response(result("修改用户信息成功", res))
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "修改用户信息失败"), status=500)
