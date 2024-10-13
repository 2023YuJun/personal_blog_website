from django.db import transaction
from django.db.models import Q
from apps.comment.models import Comment
from utils.tool import get_ip_address
from apps.user.service import get_one_user_info
from apps.like.like import get_is_like_by_id_and_type, get_is_like_by_ip_and_type


def create_comment(comment):
    """
    新增评论
    """
    with transaction.atomic():
        comment_obj = Comment.objects.create(**comment)
    return comment_obj


def apply_comment(comment):
    """
    回复评论
    """
    with transaction.atomic():
        comment_obj = Comment.objects.create(**comment)
    return comment_obj


def comment_like(comment_id):
    """
    点赞评论
    """
    comment = Comment.objects.filter(id=comment_id).first()
    if comment:
        comment.thumbs_up.increment()
    return bool(comment)


def cancel_comment_like(comment_id):
    """
    取消点赞评论
    """
    comment = Comment.objects.filter(id=comment_id).first()
    if comment:
        comment.thumbs_up.decrement()
    return bool(comment)


def delete_comment(comment_id, parent_id):
    """
    删除评论
    """
    if parent_id > 0:
        return Comment.objects.filter(id=comment_id).delete()
    else:
        Comment.objects.filter(id=comment_id).delete()
        return Comment.objects.filter(parent_id=comment_id).delete()


def back_get_comment_list(params):
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

    comments = Comment.objects.filter(where_opt).order_by('-createdAt')[size * (current - 1): size * current]
    count = Comment.objects.filter(where_opt).count()

    for r in comments:
        r.ip_address = get_ip_address()

    # 获取 from_id 和 to_id 的用户信息
    for comment in comments:
        if comment.from_id:
            user_info = get_one_user_info({'id': comment.from_id})
            if user_info:
                comment.from_avatar = user_info.avatar
                comment.from_name = user_info.nick_name
        if comment.to_id:
            user_info = get_one_user_info({'id': comment.to_id})
            if user_info:
                comment.to_avatar = user_info.avatar
                comment.to_name = user_info.nick_name

    return {
        'current': current,
        'size': size,
        'total': count,
        'list': comments,
    }


def front_get_parent_comment(params):
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

    comments = Comment.objects.filter(where_opt).order_by(order_by)[size * (current - 1): size * current]
    count = Comment.objects.filter(where_opt).count()

    for r in comments:
        r.ip_address = get_ip_address()

    # 获取 from_id 的用户信息
    for comment in comments:
        if comment.from_id:
            user_info = get_one_user_info({'id': comment.from_id})
            if user_info:
                comment.from_avatar = user_info.avatar
                comment.from_name = user_info.nick_name

    # 判断当前登录用户是否点赞了
    if user_id:
        for comment in comments:
            comment.is_like = get_is_like_by_id_and_type(
                {'for_id': comment.id, 'type': 4, 'user_id': user_id})
    else:
        for comment in comments:
            comment.is_like = get_is_like_by_ip_and_type(
                {'for_id': comment.id, 'type': 4, 'ip': ip})

    return {
        'current': current,
        'size': size,
        'total': count,
        'list': comments,
    }


def front_get_children_comment(params):
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
    comments = Comment.objects.filter(where_opt).order_by('createdAt')[size * (current - 1): size * current]
    count = Comment.objects.filter(where_opt).count()

    for r in comments:
        r.ip_address = get_ip_address()

    # 获取 from_id 和 to_id 的用户信息
    for comment in comments:
        if comment.from_id:
            user_info = get_one_user_info({'id': comment.from_id})
            if user_info:
                comment.from_avatar = user_info.avatar
                comment.from_name = user_info.nick_name
        if comment.to_id:
            user_info = get_one_user_info({'id': comment.to_id})
            if user_info:
                comment.to_avatar = user_info.avatar
                comment.to_name = user_info.nick_name

    # 判断当前登录用户是否点赞了
    if user_id:
        for comment in comments:
            comment.is_like = get_is_like_by_id_and_type(
                {'for_id': comment.id, 'type': 4, 'user_id': user_id})
    else:
        for comment in comments:
            comment.is_like = get_is_like_by_ip_and_type(
                {'for_id': comment.id, 'type': 4, 'ip': ip})

    return {
        'current': current,
        'size': size,
        'total': count,
        'list': comments,
    }


def get_comment_total(for_id, type_):
    """
    根据评论类型和类型对应的id获取评论总数
    """
    return Comment.objects.filter(for_id=for_id, type=type_).count()
