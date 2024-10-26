from django.utils import timezone
from apps.article.articleTag_service import create_article_tags
from apps.category.service import get_one_category, create_category
from apps.tag.service import get_one_tag, create_tag


def create_category_or_return(category_name, id=None):
    if id:
        return id
    else:
        one_category = get_one_category(category_name)
        if one_category:
            return one_category.id
        else:
            new_category = create_category(category_name)
            return new_category.id


def create_article_tag_by_article_id(article_id, tag_list):
    result_list = []
    # 确保 tag_list 不为空且每个标签字典都有 'tag_name' 键
    if not tag_list or any('tag_name' not in tag for tag in tag_list):
        return result_list

    # 先将新增的tag进行保存，拿到tag的id
    for tag in tag_list:
        if not tag.get('id'):
            one_tag = get_one_tag(tag['tag_name'])
            if one_tag:
                tag['id'] = one_tag.id
            else:
                new_tag = create_tag(tag)
                tag['id'] = new_tag.id

    # 文章id和标签id关联
    if article_id:
        current_time = timezone.localtime()
        article_tag_list = [
            {
                'article_id': article_id,
                'tag_id': tag['id'],
                'createdAt':current_time,
                'updatedAt': current_time,
            } for tag in tag_list
        ]
        # 批量新增文章标签关联
        result_list = create_article_tags(article_tag_list)

    return result_list
