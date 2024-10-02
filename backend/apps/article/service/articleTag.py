from django.db import transaction
from ..models import ArticleTag
from ...tag.service.tag import tag_service


class ArticleTagService:
    """
    文章标签关联表服务类
    """

    async def create_article_tags(self, tag_list):
        """
        批量增加文章标签关联
        """
        with transaction.atomic():
            res = []
            for tag in tag_list:
                article_tag = ArticleTag(**tag)
                article_tag.save()
                res.append(article_tag)

        return [v.id for v in res] if res else None

    async def delete_article_tag(self, article_id):
        """
        根据文章id删除文章标签关联
        """
        return ArticleTag.objects.filter(article_id=article_id).delete()

    async def get_tag_list_by_article_id(self, article_id):
        """
        根据文章id获取标签名称列表
        """
        res = ArticleTag.objects.filter(article_id=article_id).values_list('tag_id', flat=True)
        tag_id_list = list(res)
        tag_name_list, tag_list = await tag_service.get_tag_by_tag_id_list(tag_id_list)

        return {
            'tag_list': tag_list,
            'tag_id_list': tag_id_list,
            'tag_name_list': tag_name_list,
        }

    async def get_article_id_list_by_tag_id(self, tag_id):
        """
        根据标签id获取该标签下所有的文章id
        """
        res = ArticleTag.objects.filter(tag_id=tag_id).values_list('article_id', flat=True)
        article_id_list = list(set(res))  # 去重

        return article_id_list if article_id_list else None

    async def get_one_article_tag(self, article_id, tag_id):
        """
        查询满足的关联 存在就不用新增了 不存在就新增
        """
        return ArticleTag.objects.filter(article_id=article_id, tag_id=tag_id).exists()


# 创建服务实例
article_tag_service = ArticleTagService()
