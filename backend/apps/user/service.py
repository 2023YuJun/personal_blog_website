import re
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
from utils.sensitive import filter_sensitive
from utils.tool import random_nickname, get_ip_address
from utils.result import ERRORCODE, throw_error
from .serializers import *

error_code = ERRORCODE['USER']


def create_user(user):
    """
    用户注册
    """
    username = user.get('username')
    password = user.get('password')
    nick_name = filter_sensitive(user.get('nick_name'))

    # 随机生成昵称
    nick_name = nick_name if nick_name else random_nickname("新客")
    avatar = "http://mrzym.top/online/9bb507f4bd065759a3d093d04.webp"
    current_time = timezone.localtime()

    with transaction.atomic():
        user_obj = User.objects.create(
            username=username,
            password=make_password(password),
            nick_name=nick_name,
            avatar=avatar,
            createdAt=current_time,
            updatedAt=current_time,
            role=2
        )
    return user_obj


def update_own_user_info(user_id, user):
    """
    用户自己修改用户信息
    """
    nick_name = filter_sensitive(user.get('nick_name'))
    avatar = user.get('avatar')
    qq = user.get('qq')

    res = User.objects.filter(id=user_id).update(avatar=avatar, nick_name=nick_name, qq=qq)
    return res > 0


def update_password(user_id, password):
    """
    修改用户密码
    """
    hashed_password = make_password(password)
    res = User.objects.filter(id=user_id).update(password=hashed_password)
    return res > 0


def update_role(user_id, role):
    """
    修改用户角色
    """
    res = User.objects.filter(id=user_id).update(role=role)
    return res > 0


def get_one_user_info(filters):
    """
    根据条件查找一个用户
    """
    query_filters = Q()

    if filters.get('id'):
        query_filters &= Q(id=filters['id'])
    if filters.get('username'):
        query_filters &= Q(username=filters['username'])
    if filters.get('password'):
        query_filters &= Q(password=filters['password'])
    if filters.get('role'):
        query_filters &= Q(role=filters['role'])

    user = User.objects.filter(query_filters).defer('createdAt', 'updatedAt').first()
    return user


def get_user_list(request):
    """
    分页查询用户列表
    """
    current = request.data.get("current")
    size = request.data.get("size")
    nick_name = request.data.get("nick_name")
    role = request.data.get("role")

    offset = (current - 1) * size
    where_opt = {}

    if role is not None:
        where_opt['role'] = role
    if nick_name:
        where_opt['nick_name__icontains'] = nick_name

    users = User.objects.filter(**where_opt).defer('password')[offset:offset + size]
    total_count = User.objects.filter(**where_opt).count()

    for user in users:
        user.ip_address = get_ip_address() if user.ip else "火星"

    users = UserSerializer(users, many=True).data
    return {
        'current': current,
        'size': size,
        'total': total_count,
        'list': users,
    }


def update_ip(user_id, ip):
    """
    修改用户ip地址
    """
    res = User.objects.filter(id=user_id).update(ip=ip)
    return res > 0


def get_author_name_by_id(user_id):
    """
    根据用户id获取昵称
    """
    user = User.objects.get(pk=user_id)
    return user.nick_name if user else None


def get_user_count():
    """
    获取用户总数
    """
    return User.objects.count()


def admin_update_user_info(user_data):
    """
    管理员修改用户信息
    """
    update_count = User.objects.filter(id=user_data['id']).update(
        nick_name=user_data['nick_name'],
        avatar=user_data['avatar']
    )
    return update_count > 0


def validate_username_password(username, password):
    """
    校验用户名和密码是否为空，及用户名格式是否合法
    """
    if not username or not password:
        return JsonResponse(throw_error(error_code, "用户名或密码为空"), status=400)

    if not re.match(r"^[A-Za-z0-9]+$", username):
        return JsonResponse(throw_error(error_code, "用户名只能是数字和字母组成"), status=400)

    return None


def verify_user(username):
    """
    检查用户名是否已存在
    """
    if username == 'admin':
        return JsonResponse(throw_error(error_code, "admin账号已存在"), status=400)

    res = get_one_user_info({'username': username})
    if res:
        return JsonResponse(throw_error(error_code, "用户名已经存在"), status=400)

    return None


def verify_login_credentials(username, password):
    """
    验证登录时的用户名和密码
    """
    if username != 'admin':
        res = get_one_user_info({'username': username})

        if not res:
            return JsonResponse(throw_error(error_code, "用户名不存在"), status=400)

        if not check_password(password, res.password):
            return JsonResponse(throw_error(error_code, "密码不匹配"), status=400)

    return None


def verify_update_password(username, current_password, new_password1, new_password2):
    """
    更新密码时验证当前密码和新密码
    """
    if username != 'admin':
        if new_password1 != new_password2:
            return JsonResponse(throw_error(error_code, "两次输入密码不一致"), status=400)

        res = get_one_user_info({'username': username})

        if not check_password(current_password, res.password):
            return JsonResponse(throw_error(error_code, "密码不匹配"), status=400)
    else:
        return JsonResponse(throw_error(error_code, "admin密码只可以通过配置文件env修改"), status=400)

    return None
