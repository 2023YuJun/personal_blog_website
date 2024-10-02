from .models import ArticleTag
from .service.articleTag import article_tag_service
from ..category.service.category import category_service
from ..tag.service.tag import tag_service


async def create_category_or_return(category_name, id=None):
    if id:
        return id
    else:
        one_category = await category_service.get_one_category(category_name)
        if one_category:
            return one_category.id
        else:
            new_category = await category_service.create_category(category_name)
            return new_category.id


async def create_article_tag_by_article_id(article_id, tag_list):
    result_list = []

    # 先将新增的tag进行保存，拿到tag的id
    for tag in tag_list:
        if not tag.get('id'):
            one_tag = await tag_service.get_one_tag(tag['tag_name'])
            if one_tag:
                tag['id'] = one_tag.id
            else:
                new_tag = await tag_service.create_tag(tag)
                tag['id'] = new_tag.id

    # 文章id和标签id关联
    if article_id:
        article_tag_list = [
            ArticleTag(article_id=article_id, tag_id=tag['id']) for tag in tag_list
        ]
        # 批量新增文章标签关联
        result_list = await article_tag_service.create_article_tags(article_tag_list)

    return result_list
