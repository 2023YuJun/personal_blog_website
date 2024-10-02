from ..models import Message  # 根据你的项目结构调整导入路径
from ...user.service.user import user_service
from ...like.service.like import like_service
from ...comment.service.comment import comment_service
from django.db.models import Q
import asyncio


class MessageService:
    """
    留言服务层
    """

    async def add_message(self, message_data):
        """
        发布留言
        """
        await Message.objects.create(**message_data)
        return True

    async def update_message(self, message_data):
        """
        修改留言
        """
        id = message_data.get('id')
        await Message.objects.filter(id=id).update(**message_data)
        return True

    async def delete_message(self, id_list):
        """
        根据id列表删除留言
        """
        res = await Message.objects.filter(id__in=id_list).delete()
        return res if res else None

    async def message_like(self, id):
        """
        点赞留言
        """
        message = await Message.objects.filter(id=id).first()
        if message:
            await message.increment("like_times", by=1)
        return True if message else False

    async def cancel_message_like(self, id):
        """
        取消点赞留言
        """
        message = await Message.objects.filter(id=id).first()
        if message:
            await message.decrement("like_times", by=1)
        return True if message else False

    async def get_message_list(self, current, size, message=None, time=None, tag=None, user_id=None, ip=None):
        """
        分页获取留言
        """
        offset = (current - 1) * size
        where_opt = Q()

        if tag:
            where_opt &= Q(tag=tag)
        if message:
            where_opt &= Q(message__icontains=message)
        if time:
            where_opt &= Q(createdAt__range=time)

        rows = await Message.objects.filter(where_opt).order_by("-createdAt")[offset:offset + size]
        total_count = await Message.objects.filter(where_opt).count()

        # 根据用户form_id获取用户当前的昵称和头像
        promise_list = []
        for row in rows:
            if row.user_id:
                promise_list.append(user_service.get_one_user_info({"id": row.user_id}))
            else:
                promise_list.append({"nick_name": row.nick_name, "avatar": ""})

        user_info_results = await asyncio.gather(*promise_list)
        for index, user_info in enumerate(user_info_results):
            if isinstance(user_info, dict):
                rows[index].nick_name = user_info['nick_name']
                rows[index].avatar = user_info['avatar']

        # 判断当前登录用户是否点赞了
        if user_id:
            like_checks = [like_service.get_is_like_by_id_and_type({"for_id": row.id, "type": 3, "user_id": user_id})
                           for row in rows]
        else:
            like_checks = [like_service.get_is_like_by_ip_and_type({"for_id": row.id, "type": 3, "ip": ip}) for row in
                           rows]

        like_results = await asyncio.gather(*like_checks)
        for index, is_like in enumerate(like_results):
            rows[index].is_like = is_like

        # 获取每一条的评论条数
        comment_checks = [comment_service.get_comment_total({"for_id": row.id, "type": 3}) for row in rows]
        comment_results = await asyncio.gather(*comment_checks)
        for index, comment_total in enumerate(comment_results):
            rows[index].comment_total = comment_total

        return {
            "current": current,
            "size": size,
            "list": rows,
            "total": total_count,
        }

    async def get_all_message(self):
        """
        获取所有留言
        """
        rows = await Message.objects.order_by("-createdAt").all()
        promise_list = []

        for row in rows:
            if row.user_id:
                promise_list.append(user_service.get_one_user_info({"id": row.user_id}))
            else:
                promise_list.append({"nick_name": row.nick_name, "avatar": ""})

        user_info_results = await asyncio.gather(*promise_list)
        for index, user_info in enumerate(user_info_results):
            if isinstance(user_info, dict):
                rows[index].nick_name = user_info['nick_name']
                rows[index].avatar = user_info['avatar']

        return {
            "list": rows,
            "total": len(rows),
        }

    async def get_message_tag(self):
        """
        获取热门的标签
        """
        all_messages = await Message.objects.all()
        tag_counts = {}

        for message in all_messages:
            tag = message.tag
            if tag:
                if tag not in tag_counts:
                    tag_counts[tag] = 0
                tag_counts[tag] += 1

        # 按照出现次数排序并返回前10个
        sorted_tags = sorted(tag_counts.items(), key=lambda item: item[1], reverse=True)
        return [{"tag": tag, "count": count} for tag, count in sorted_tags[:10]]


# 创建服务实例
message_service = MessageService()
