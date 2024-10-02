from django.contrib.auth.hashers import make_password
from django.db import transaction
from utils.sensitive import filter_sensitive
from utils.tool import random_nickname, get_ip_address

from ..models import User


class UserService:
    """
    用户服务层
    """

    async def create_user(self, user):
        """
        用户注册
        """
        username = user.get('username')
        password = user.get('password')
        nick_name = await filter_sensitive(user.get('nick_name'))
        qq = user.get('qq')

        # 随机生成昵称
        nick_name = nick_name if nick_name else random_nickname("新客")
        avatar = "http://mrzym.top/online/9bb507f4bd065759a3d093d04.webp"

        async with transaction.atomic():
            user_obj = await User.objects.create(
                username=username,
                password=make_password(password),
                nick_name=nick_name,
                qq=qq,
                avatar=avatar,
                role=2
            )
        return user_obj

    async def update_own_user_info(self, user_id, user):
        """
        用户自己修改用户信息
        """
        nick_name = await filter_sensitive(user.get('nick_name'))
        avatar = user.get('avatar')
        qq = user.get('qq')

        res = await User.objects.filter(id=user_id).update(avatar=avatar, nick_name=nick_name, qq=qq)
        return res > 0

    async def update_password(self, user_id, password):
        """
        修改用户密码
        """
        hashed_password = make_password(password)
        res = await User.objects.filter(id=user_id).update(password=hashed_password)
        return res > 0

    async def update_role(self, user_id, role):
        """
        修改用户角色
        """
        res = await User.objects.filter(id=user_id).update(role=role)
        return res > 0

    async def get_one_user_info(self, filters):
        """
        根据条件查找一个用户
        """
        user = await User.objects.filter(**filters).exclude('created_at', 'updated_at').first()
        return user if user else None

    async def get_user_list(self, params):
        """
        分页查询用户列表
        """
        current = params.get('current', 1)
        size = params.get('size', 10)
        nick_name = params.get('nick_name')
        role = params.get('role')

        offset = (current - 1) * size
        where_opt = {}

        if role is not None:
            where_opt['role'] = role
        if nick_name:
            where_opt['nick_name__icontains'] = nick_name

        users = await User.objects.filter(**where_opt).exclude('password')[offset:offset + size]
        total_count = await User.objects.filter(**where_opt).count()

        for user in users:
            user.ip_address = get_ip_address(user.ip) if user.ip else "火星"

        return {
            'current': current,
            'size': len(users),
            'total': total_count,
            'list': users,
        }

    async def update_ip(self, user_id, ip):
        """
        修改用户ip地址
        """
        res = await User.objects.filter(id=user_id).update(ip=ip)
        return res > 0

    async def get_author_name_by_id(self, user_id):
        """
        根据用户id获取昵称
        """
        user = await User.objects.get(pk=user_id)
        return user.nick_name if user else None

    async def get_user_count(self):
        """
        获取用户总数
        """
        return await User.objects.count()

    async def admin_update_user_info(self, user_id, nick_name, avatar):
        """
        管理员修改用户信息
        """
        res = await User.objects.filter(id=user_id).update(nick_name=nick_name, avatar=avatar)
        return res > 0


# 创建服务实例
user_service = UserService()
