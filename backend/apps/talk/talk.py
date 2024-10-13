from apps.talk.models import Talk  # 根据你的项目结构调整导入路径
from apps.talk.talkPhoto import publish_talk_photo, delete_talk_photo, get_photo_by_talk_id
from apps.user.service import get_one_user_info
from apps.like.like import get_is_like_by_id_and_type, get_is_like_by_ip_and_type


def publish_talk(talk):
    """
    新增说说
    """
    talk_img_list = talk.pop('talkImgList', [])
    res = Talk.objects.create(**talk)

    if res.id:
        img_list = [{'talk_id': res.id, 'url': img['url']} for img in talk_img_list]
        publish_talk_photo(img_list)

    return res


def update_talk(talk):
    """
    修改说说
    """
    id = talk.pop('id')
    talk_img_list = talk.pop('talkImgList', [])
    res = Talk.objects.filter(id=id).update(**talk)

    delete_talk_photo(id)
    img_list = [{'talk_id': id, 'url': img['url']} for img in talk_img_list]
    publish_talk_photo(img_list)

    return res > 0


def delete_talk_by_id(id, status):
    """
    删除说说
    """
    if status in [1, 2]:
        res = Talk.objects.filter(id=id).update(status=3)
    else:
        res = Talk.objects.filter(id=id).delete()
        delete_talk_photo(id)

    return res


def toggle_public(id, status):
    """
    切换说说公开性
    """
    res = Talk.objects.filter(id=id).update(status=status)
    return res > 0


def revert_talk(id):
    """
    恢复说说
    """
    res = Talk.objects.filter(id=id).update(status=1)
    return res > 0


def toggle_top(id, is_top):
    """
    置顶/取消置顶说说
    """
    res = Talk.objects.filter(id=id).update(is_top=is_top)
    return res > 0


def talk_like(id):
    """
    说说点赞
    """
    talk = Talk.objects.get(id=id)
    if talk:
        talk.increment('like_times', by=1)
    return bool(talk)


def cancel_talk_like(id):
    """
    取消说说点赞
    """
    talk = Talk.objects.get(id=id)
    if talk:
        talk.decrement('like_times', by=1)
    return bool(talk)


def get_talk_list(current, size, status):
    """
    获取说说列表
    """
    offset = (current - 1) * size
    limit = size

    where_opt = {}
    if status:
        where_opt['status'] = status

    rows, count = Talk.objects.filter(**where_opt).order_by('is_top', '-createdAt')[
                  offset:offset + limit], Talk.objects.filter(**where_opt).count()

    # 处理图片
    for row in rows:
        row.talkImgList = get_photo_by_talk_id(row.id)
        # 获取用户信息

    for row in rows:
        user_info = get_one_user_info({'id': row.user_id})
        if user_info:
            row.nick_name = user_info.nick_name
            row.avatar = user_info.avatar

    return {
        'current': current,
        'size': size,
        'list': rows,
        'total': count,
    }


def get_talk_by_id(id):
    """
    根据id获取说说详情
    """
    res = Talk.objects.get(id=id)
    imgs = get_photo_by_talk_id(id)

    return {
        **res,
        'talkImgList': [img.url for img in imgs],
    }


def blog_get_talk_list(current, size, user_id, ip):
    """
    前台获取说说列表
    """
    offset = (current - 1) * size
    limit = size

    rows, count = Talk.objects.filter(status=1).order_by('is_top', '-createdAt')[
                  offset:offset + limit], Talk.objects.filter(status=1).count()

    # 处理图片
    for row in rows:
        row.talkImgList = get_photo_by_talk_id(row.id)

    # 获取用户信息
    for row in rows:
        user_info = get_one_user_info({'id': row.user_id})
        if user_info:
            row.nick_name = user_info.nick_name
            row.avatar = user_info.avatar

    # 判断当前登录用户是否点赞了
    if user_id:
        for row in rows:
            row.is_like = get_is_like_by_id_and_type({'for_id': row.id, 'type': 2, 'user_id': user_id})
    else:
        for row in rows:
            row.is_like = get_is_like_by_ip_and_type({'for_id': row.id, 'type': 2, 'ip': ip})

    return {
        'current': current,
        'size': size,
        'list': rows,
        'total': count,
    }

