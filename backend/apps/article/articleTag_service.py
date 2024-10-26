from django.db import transaction
from apps.article.models import ArticleTag
from apps.tag.service import get_tag_by_tag_id_list


def create_article_tags(tag_list):
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


def delete_article_tag(article_id):
    """
    根据文章id删除文章标签关联
    """
    return ArticleTag.objects.filter(article_id=article_id).delete()


def get_tag_list_by_article_id(article_id):
    """
    根据文章id获取标签名称列表
    """
    res = ArticleTag.objects.filter(article_id=article_id).values_list('tag_id', flat=True)
    tag_id_list = list(res)
    result = get_tag_by_tag_id_list(tag_id_list)
    tag_name_list = result.get("tagNameList", [])
    tag_list = result.get("tagList", [])

    return {
        'tag_list': tag_list,
        'tag_id_list': tag_id_list,
        'tag_name_list': tag_name_list,
    }


def get_article_id_list_by_tag_id(tag_ids):
    """
    根据标签id获取该标签下所有的文章id
    """
    res = ArticleTag.objects.filter(tag_id__in=tag_ids).values_list('article_id', flat=True)
    article_id_list = list(set(res))  # 去重

    return article_id_list


def get_one_article_tag(article_id, tag_id):
    """
    查询满足的关联 存在就不用新增了 不存在就新增
    """
    return ArticleTag.objects.filter(article_id=article_id, tag_id=tag_id).exists()
