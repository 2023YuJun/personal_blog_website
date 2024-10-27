from django.db import transaction
from django.db.models import F
from django.utils import timezone

from apps.like.service import get_is_like_by_id_and_type, get_is_like_by_ip_and_type
from apps.talk.talkPhoto_service import publish_talk_photo, delete_talk_photo, get_photo_by_talk_id
from apps.user.service import get_one_user_info
from .models import Talk
from .serializers import TalkSerializer


def publish_talk(talk):
    """
    新增说说
    """
    talk_img_list = talk.pop('talkImgList', [])
    current_time = timezone.localtime()
    talk['createdAt'] = current_time
    talk['updatedAt'] = current_time
    with transaction.atomic():
        res = Talk.objects.create(**talk)

        if res.id and talk_img_list:
            img_list = [
                {
                    'talk_id': res.id,
                    'url': img['url'],
                    'createdAt': current_time,
                    'updatedAt': current_time
                }
                for img in talk_img_list
            ]
            publish_talk_photo(img_list)

    return res


def update_talk(talk):
    """
    修改说说
    """
    talk.pop('createdAt', None)
    talk.pop('updatedAt', None)
    id = talk.get('id')
    current_time = timezone.localtime()
    talk_img_list = talk.pop('talkImgList', [])
    model_fields = {field.name for field in Talk._meta.get_fields()}
    valid_talk = {key: value for key, value in talk.items() if key in model_fields}
    res = Talk.objects.filter(id=id).update(**valid_talk, updatedAt=current_time)

    delete_talk_photo(id)
    img_list = [
        {
            'talk_id': id,
            'url': img['url'],
            'createdAt': current_time,
            'updatedAt': current_time
        } for img in talk_img_list
    ]
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
    updated_count = Talk.objects.filter(pk=id).update(like_times=F('like_times') + 1)
    return updated_count > 0


def cancel_talk_like(id):
    """
    取消说说点赞
    """
    updated_count = Talk.objects.filter(pk=id).update(like_times=F('like_times') - 1)
    return updated_count > 0


def get_talk_list(current, size, status):
    """
    获取说说列表
    """
    offset = (current - 1) * size
    limit = size

    where_opt = {}
    if status:
        where_opt['status'] = status

    rows = Talk.objects.filter(**where_opt).order_by('is_top', '-createdAt')[offset:offset + limit]
    count = Talk.objects.filter(**where_opt).count()

    rows = TalkSerializer(rows, many=True).data

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

    talk_data = TalkSerializer(res).data
    talk_data['talkImgList'] = [img['url'] for img in imgs]

    return talk_data


def blog_get_talk_list(current, size, user_id, ip):
    """
    前台获取说说列表
    """
    offset = (current - 1) * size
    limit = size

    rows = Talk.objects.filter(status=1).order_by('is_top', '-createdAt')[offset:offset + limit]
    count = Talk.objects.filter(status=1).count()
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
            row.is_like = get_is_like_by_id_and_type(row.id, 2, user_id)
    else:
        for row in rows:
            row.is_like = get_is_like_by_ip_and_type(row.id, 2, ip)

    rows = TalkSerializer(rows, many=True).data

    return {
        'current': current,
        'size': size,
        'list': rows,
        'total': count,
    }
