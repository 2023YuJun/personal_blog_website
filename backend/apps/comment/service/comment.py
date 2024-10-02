from django.db import transaction
from django.db.models import Q
from ..models import Comment  # 根据你的项目结构调整导入路径
from utils.tool import get_ip_address
from ...user.service.user import user_service  # 导入用户信息获取函数
from ...like.service.like import like_service  # 导入点赞功能


class CommentService:
    """
    评论服务层
    """

    async def create_comment(self, comment):
        """
        新增评论
        """
        async with transaction.atomic():
            comment_obj = await Comment.objects.create(**comment)
        return comment_obj

    async def apply_comment(self, comment):
        """
        回复评论
        """
        async with transaction.atomic():
            comment_obj = await Comment.objects.create(**comment)
        return comment_obj

    async def comment_like(self, comment_id):
        """
        点赞评论
        """
        comment = await Comment.objects.filter(id=comment_id).first()
        if comment:
            await comment.thumbs_up.increment()  # 假设你在 Comment 模型中有 thumbs_up 字段
        return bool(comment)

    async def cancel_comment_like(self, comment_id):
        """
        取消点赞评论
        """
        comment = await Comment.objects.filter(id=comment_id).first()
        if comment:
            await comment.thumbs_up.decrement()  # 假设你在 Comment 模型中有 thumbs_up 字段
        return bool(comment)

    async def delete_comment(self, comment_id, parent_id):
        """
        删除评论
        """
        if parent_id > 0:
            return await Comment.objects.filter(id=comment_id).delete()
        else:
            await Comment.objects.filter(id=comment_id).delete()
            return await Comment.objects.filter(parent_id=comment_id).delete()

    async def back_get_comment_list(self, params):
        """
        后台分页获取评论列表
        """
        current = params.get('current', 1)
        size = params.get('size', 10)
        content = params.get('content')
        to_name = params.get('to_name')
        from_name = params.get('from_name')
        time = params.get('time')

        where_opt = Q()
        if content:
            where_opt &= Q(content__icontains=content)
        if to_name:
            where_opt &= Q(to_name__icontains=to_name)
        if from_name:
            where_opt &= Q(from_name__icontains=from_name)
        if time:
            where_opt &= Q(createdAt__range=time)

        comments = await Comment.objects.filter(where_opt).order_by('-createdAt')[size * (current - 1): size * current]
        count = await Comment.objects.filter(where_opt).count()

        for r in comments:
            r.ip_address = get_ip_address(r.ip)

        # 获取 from_id 和 to_id 的用户信息
        for comment in comments:
            if comment.from_id:
                user_info = await user_service.get_one_user_info({'id': comment.from_id})
                if user_info:
                    comment.from_avatar = user_info.avatar
                    comment.from_name = user_info.nick_name
            if comment.to_id:
                user_info = await user_service.get_one_user_info({'id': comment.to_id})
                if user_info:
                    comment.to_avatar = user_info.avatar
                    comment.to_name = user_info.nick_name

        return {
            'current': current,
            'size': size,
            'total': count,
            'list': comments,
        }

    async def front_get_parent_comment(self, params):
        """
        前台分页获取父级评论
        """
        current = params.get('current', 1)
        size = params.get('size', 10)
        type_ = params.get('type')
        for_id = params.get('for_id')
        user_id = params.get('user_id')
        order = params.get('order')
        ip = params.get('ip')

        where_opt = Q(type=type_) & Q(for_id=for_id) & Q(parent_id=None)
        order_by = 'createdAt' if order == 'new' else 'thumbs_up'

        comments = await Comment.objects.filter(where_opt).order_by(order_by)[size * (current - 1): size * current]
        count = await Comment.objects.filter(where_opt).count()

        for r in comments:
            r.ip_address = get_ip_address(r.ip)

        # 获取 from_id 的用户信息
        for comment in comments:
            if comment.from_id:
                user_info = await user_service.get_one_user_info({'id': comment.from_id})
                if user_info:
                    comment.from_avatar = user_info.avatar
                    comment.from_name = user_info.nick_name

        # 判断当前登录用户是否点赞了
        if user_id:
            for comment in comments:
                comment.is_like = await like_service.get_is_like_by_id_and_type(
                    {'for_id': comment.id, 'type': 4, 'user_id': user_id})
        else:
            for comment in comments:
                comment.is_like = await like_service.get_is_like_by_ip_and_type(
                    {'for_id': comment.id, 'type': 4, 'ip': ip})

        return {
            'current': current,
            'size': size,
            'total': count,
            'list': comments,
        }

    async def front_get_children_comment(self, params):
        """
        前台分页获取子评论
        """
        current = params.get('current', 1)
        size = params.get('size', 10)
        type_ = params.get('type')
        for_id = params.get('for_id')
        parent_id = params.get('parent_id')
        user_id = params.get('user_id')
        ip = params.get('ip')

        where_opt = Q(type=type_) & Q(for_id=for_id) & Q(parent_id=parent_id)
        comments = await Comment.objects.filter(where_opt).order_by('createdAt')[size * (current - 1): size * current]
        count = await Comment.objects.filter(where_opt).count()

        for r in comments:
            r.ip_address = get_ip_address(r.ip)

        # 获取 from_id 和 to_id 的用户信息
        for comment in comments:
            if comment.from_id:
                user_info = await user_service.get_one_user_info({'id': comment.from_id})
                if user_info:
                    comment.from_avatar = user_info.avatar
                    comment.from_name = user_info.nick_name
            if comment.to_id:
                user_info = await user_service.get_one_user_info({'id': comment.to_id})
                if user_info:
                    comment.to_avatar = user_info.avatar
                    comment.to_name = user_info.nick_name

        # 判断当前登录用户是否点赞了
        if user_id:
            for comment in comments:
                comment.is_like = await like_service.get_is_like_by_id_and_type(
                    {'for_id': comment.id, 'type': 4, 'user_id': user_id})
        else:
            for comment in comments:
                comment.is_like = await like_service.get_is_like_by_ip_and_type(
                    {'for_id': comment.id, 'type': 4, 'ip': ip})

        return {
            'current': current,
            'size': size,
            'total': count,
            'list': comments,
        }

    async def get_comment_total(self, for_id, type_):
        """
        根据评论类型和类型对应的id获取评论总数
        """
        return await Comment.objects.filter(for_id=for_id, type=type_).count()


# 创建服务实例
comment_service = CommentService()
