from ..models import Talk  # 根据你的项目结构调整导入路径
from .talkPhoto import talk_photo_service
from ...user.service.user import user_service
from ...like.service.like import like_service
import asyncio


class TalkService:
    """
    说说服务层
    """

    async def publish_talk(self, talk):
        """
        新增说说
        """
        talk_img_list = talk.pop('talkImgList', [])
        res = await Talk.objects.create(**talk)

        if res.id:
            img_list = [{'talk_id': res.id, 'url': img['url']} for img in talk_img_list]
            await talk_photo_service.publish_talk_photo(img_list)

        return res

    async def update_talk(self, talk):
        """
        修改说说
        """
        id = talk.pop('id')
        talk_img_list = talk.pop('talkImgList', [])
        res = await Talk.objects.filter(id=id).update(**talk)

        await talk_photo_service.delete_talk_photo(id)
        img_list = [{'talk_id': id, 'url': img['url']} for img in talk_img_list]
        await talk_photo_service.publish_talk_photo(img_list)

        return res > 0

    async def delete_talk_by_id(self, id, status):
        """
        删除说说
        """
        if status in [1, 2]:
            res = await Talk.objects.filter(id=id).update(status=3)
        else:
            res = await Talk.objects.filter(id=id).delete()
            await talk_photo_service.delete_talk_photo(id)

        return res

    async def toggle_public(self, id, status):
        """
        切换说说公开性
        """
        res = await Talk.objects.filter(id=id).update(status=status)
        return res > 0

    async def revert_talk(self, id):
        """
        恢复说说
        """
        res = await Talk.objects.filter(id=id).update(status=1)
        return res > 0

    async def toggle_top(self, id, is_top):
        """
        置顶/取消置顶说说
        """
        res = await Talk.objects.filter(id=id).update(is_top=is_top)
        return res > 0

    async def talk_like(self, id):
        """
        说说点赞
        """
        talk = await Talk.objects.get(id=id)
        if talk:
            await talk.increment('like_times', by=1)
        return bool(talk)

    async def cancel_talk_like(self, id):
        """
        取消说说点赞
        """
        talk = await Talk.objects.get(id=id)
        if talk:
            await talk.decrement('like_times', by=1)
        return bool(talk)

    async def get_talk_list(self, current, size, status):
        """
        获取说说列表
        """
        offset = (current - 1) * size
        limit = size

        where_opt = {}
        if status:
            where_opt['status'] = status

        rows, count = await Talk.objects.filter(**where_opt).order_by('is_top', '-createdAt')[offset:offset + limit], await Talk.objects.filter(**where_opt).count()

        # 处理图片
        for row in rows:
            row.talkImgList = await talk_photo_service.get_photo_by_talk_id(row.id)

        user_promises = [user_service.get_one_user_info({'id': row.user_id}) for row in rows]
        users = await asyncio.gather(*user_promises)

        for user, row in zip(users, rows):
            if user:
                row.nick_name = user.nick_name
                row.avatar = user.avatar

        return {
            'current': current,
            'size': size,
            'list': rows,
            'total': count,
        }

    async def get_talk_by_id(self, id):
        """
        根据id获取说说详情
        """
        res = await Talk.objects.get(id=id)
        imgs = await talk_photo_service.get_photo_by_talk_id(id)

        return {
            **res,
            'talkImgList': [img.url for img in imgs],
        }

    async def blog_get_talk_list(self, current, size, user_id, ip):
        """
        前台获取说说列表
        """
        offset = (current - 1) * size
        limit = size

        rows, count = await Talk.objects.filter(status=1).order_by('is_top', '-createdAt')[offset:offset + limit], await Talk.objects.filter(status=1).count()

        # 处理图片
        for row in rows:
            row.talkImgList = await talk_photo_service.get_photo_by_talk_id(row.id)

        user_promises = [user_service.get_one_user_info({'id': row.user_id}) for row in rows]
        users = await asyncio.gather(*user_promises)

        for user, row in zip(users, rows):
            if user:
                row.nick_name = user.nick_name
                row.avatar = user.avatar

        # 判断当前登录用户是否点赞了
        if user_id:
            like_promises = [like_service.get_is_like_by_id_and_type({'for_id': row.id, 'type': 2, 'user_id': user_id}) for row in rows]
            results = await asyncio.gather(*like_promises)
            for result, row in zip(results, rows):
                row.is_like = result
        else:
            like_promises = [like_service.get_is_like_by_ip_and_type({'for_id': row.id, 'type': 2, 'ip': ip}) for row in rows]
            results = await asyncio.gather(*like_promises)
            for result, row in zip(results, rows):
                row.is_like = result

        return {
            'current': current,
            'size': size,
            'list': rows,
            'total': count,
        }

# 创建服务实例
talk_service = TalkService()
