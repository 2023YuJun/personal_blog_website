from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user.service import *
from utils.minioUpload import delete_minio_imgs
from utils.result import result
from utils.tool import get_ip_address

error_code = ERRORCODE['USER']


class UserView(APIView):
    """用户控制器"""

    def post(self, request, *args, **kwargs):
        if 'register' in request.path:
            return self.register(request)
        elif 'login' in request.path:
            return self.login(request)
        elif 'getUserList' in request.path:
            return self.get_user_list(request)

    def put(self, request, *args, **kwargs):
        if 'updateOwnUserInfo' in request.path:
            return self.update_own_user_info(request)
        elif 'updatePassword' in request.path:
            return self.update_password(request)
        elif 'updateRole' in request.path:
            return self.update_role(request, kwargs.get('id'), kwargs.get('role'))
        elif 'adminUpdateUserInfo' in request.path:
            return self.admin_update_user_info(request)

    def get(self, request, *args, **kwargs):
        if 'getUserInfoById' in request.path:
            return self.get_user_info(request, kwargs.get('id'))

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
            response = validate_username_password(username, password)
            if response is None:
                response = verify_login_credentials(username, password)
                if response is None:
                    if username == "admin":
                        if password == settings.ADMIN_PASSWORD:
                            token = jwt.encode(
                                {"nick_name": "超级管理员", "id": 5201314, "role": 1, "username": "admin"},
                                settings.JWT_SECRET, algorithm="HS256")
                            return JsonResponse(result("超级管理员登录成功",
                                                       {"token": token, "username": "超级管理员", "role": 1,
                                                        "id": 5201314}))
                        else:
                            return JsonResponse(throw_error(error_code, "密码错误"), status=400)
                    else:
                        res = get_one_user_info({"username": username})
                        ip = request.META.get("HTTP_X_REAL_IP") or request.META.get(
                            "HTTP_X_FORWARDED_FOR") or request.META.get(
                            "REMOTE_ADDR")
                        update_ip(res.id, ip.split(":")[-1])
                        ip_address = get_ip_address()
                        token = jwt.encode(
                            {"id": res.id, "username": res.username, "role": res.role, "nick_name": res.nick_name},
                            settings.JWT_SECRET, algorithm="HS256")
                        return JsonResponse(result("用户登录成功",
                                                   {"token": token, "username": res.username, "role": res.role,
                                                    "id": res.id, "ipAddress": ip_address}), status=200)
                else:
                    return response
            else:
                return response
        except Exception as err:
            print(err)
            return JsonResponse(throw_error(error_code, "用户登陆失败"), status=500)

    def update_own_user_info(self, request):
        """用户修改自己的用户信息"""
        try:
            user_id = request.payload['id']
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
            user_id = request.payload['id']
            username = request.payload['username']
            current_password = request.data.get("password")
            password1 = request.data.get("password1")
            password2 = request.data.get("password2")

            if user_id == 2:
                return Response(throw_error(error_code, "测试用户密码不可以修改哦"), status=400)

            response = verify_update_password(username, current_password, password1, password2)
            if response is None:
                res = update_password(user_id, password1)
                return Response(result("修改用户密码成功", res))
            else:
                return response
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
                if res:
                    # 将模型实例转换为字典
                    res_info = model_to_dict(res, exclude=["password", "username", "ip"])
                    res_info["ipAddress"] = ip_address
                    return Response(result("获取用户信息成功", res_info), status=200)
                else:
                    return Response(throw_error(error_code, "用户不存在"), status=404)
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
