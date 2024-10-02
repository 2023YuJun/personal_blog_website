from ..models import Like  # 根据你的项目结构调整导入路径


class LikeService:
    """
    点赞服务层
    """

    async def add_like(self, like_data):
        """
        点赞
        """
        await Like.objects.create(**like_data)
        return True

    async def cancel_like(self, for_id, type, user_id=None, ip=None):
        """
        根据 for_id、type、user_id 取消点赞
        """
        where_opt = {'for_id': for_id, 'type': type}
        if ip:
            where_opt['ip'] = ip
        if user_id:
            where_opt['user_id'] = user_id

        res = await Like.objects.filter(**where_opt).delete()
        return res if res else None

    async def get_is_like_by_id_and_type(self, for_id, type, user_id):
        """
        获取当前用户对当前文章/说说/留言是否点赞
        """
        like_exists = await Like.objects.filter(for_id=for_id, type=type, user_id=user_id).exists()
        return like_exists

    async def get_is_like_by_ip_and_type(self, for_id, type, ip):
        """
        获取当前ip对当前文章/说说/留言是否点赞
        """
        like_exists = await Like.objects.filter(for_id=for_id, type=type, ip=ip).exists()
        return like_exists


# 创建服务实例
like_service = LikeService()
