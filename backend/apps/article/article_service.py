from django.db import transaction
from django.db.models import Q
from .serializers import *
from django.utils import timezone
from apps.article.articleTag_service import delete_article_tag, get_tag_list_by_article_id, get_article_id_list_by_tag_id
from apps.category.service import get_category_name_by_id
from apps.user.service import get_author_name_by_id
from utils.result import ERRORCODE, throw_error
from rest_framework.response import Response

error_code = ERRORCODE['ARTICLE']


def update_url():
    """
    批量替换url
    """
    articles = Article.objects.all()
    for article in articles:
        article.article_cover = article.article_cover.replace("http://img.mrzym.top/", "http://mrzym.top/online/")
        article.save()


def create_article(article_data):
    """
    新增文章
    """
    try:
        with transaction.atomic():
            current_time = timezone.localtime()
            article = Article.objects.create(**article_data, createdAt=current_time, updatedAt=current_time)
            res = ArticleSerializer(article, many=True).data
            return res
    except Exception as e:
        print(e)
        return None


def update_article(article_data):
    """
    修改文章信息
    """
    try:
        with transaction.atomic():
            current_time = timezone.localtime()
            article = Article.objects.get(pk=article_data['id'])
            for attr, value in article_data.items():
                setattr(article, attr, value)
            article.updatedAt = current_time
            res = article.save()
            res = ArticleSerializer(res, many=True).data
            return res
    except Article.DoesNotExist:
        return None
    except Exception as e:
        print(e)
        return None


def update_top(article_id, is_top):
    """
    修改文章置顶信息
    """
    return Article.objects.filter(id=article_id).update(is_top=is_top) > 0


def delete_article(article_id, status):
    """
    删除文章
    """
    if status != 3:
        return Article.objects.filter(id=article_id).update(status=3) > 0
    else:
        with transaction.atomic():
            delete_article_tag(article_id)
            return Article.objects.filter(id=article_id).delete() > 0


def revert_article(article_id):
    """
    恢复文章
    """
    return Article.objects.filter(id=article_id).update(status=1) > 0


def toggle_article_public(article_id, status):
    """
    公开或隐藏文章
    """
    new_status = 1 if status == 2 else 2
    return Article.objects.filter(id=article_id).update(status=new_status) > 0


def get_article_info_by_title(title, article_id=None):
    """
    根据文章标题获取文章信息
    """
    article = Article.objects.filter(article_title=title).first()
    if article:
        return article.id != article_id if article_id else True
    return False


def get_article_list(params):
    """
    同步条件分页查询文章列表
    """
    current = params.get('current', 1)
    size = params.get('size', 10)
    offset = (current - 1) * size

    query = Q()

    if 'article_title' in params and params['article_title'] is not None:
        query &= Q(article_title__icontains=params['article_title'])
    if 'create_time' in params and params['create_time'] is not None:
        query &= Q(createdAt__range=params['create_time'])
    if 'is_top' in params and params['is_top'] is not None:
        query &= Q(is_top=params['is_top'])
    if 'status' in params and params['status'] is not None:
        query &= Q(status=params['status'])
    else:
        query &= Q(status__in=[1, 2])
    if 'category_id' in params and params['category_id'] is not None:
        query &= Q(category_id=params['category_id'])

    # 根据标签id查文章
    if 'tag_id' in params and params['tag_id'] is not None:
        article_ids = get_article_id_list_by_tag_id(params['tag_id'])
        if article_ids:
            query &= Q(id__in=article_ids)

    # 获取文章列表
    articles = Article.objects.filter(query).exclude(article_content__in=["", None]).order_by('-createdAt')[offset:offset + size]
    total_count = Article.objects.filter(query).count()

    # 根据文章id获取文章的标签名称和分类名称
    for article in articles:
        article.category_name = get_category_name_by_id(article.category_id)
        article.tag_name_list = get_tag_list_by_article_id(article.id)

    articles = ArticleSerializer(articles, many=True).data
    return {
        'current': current,
        'size': size,
        'list': articles,
        'total': total_count,
    }


def get_article_by_id(article_id):
    """
    根据文章id获取文章详细信息
    """
    article = Article.objects.get(pk=article_id)
    if article:
        article.increment('view_times', by=1)
        article.tag_id_list = get_tag_list_by_article_id(article_id)
        article.category_name = get_category_name_by_id(article.category_id)
        article.author_name = get_author_name_by_id(article.author_id)
        return article
    return None


def blog_home_get_article_list(current, size):
    """
    博客前台获取文章列表
    """
    offset = (current - 1) * size
    articles = Article.objects.filter(status=1).order_by('is_top', 'order', '-createdAt')[offset:offset + size]
    total_count = Article.objects.filter(status=1).count()

    for article in articles:
        article.category_name = get_category_name_by_id(article.category_id)
        article.tag_name_list = get_tag_list_by_article_id(article.id)

    articles = ArticleSerializer(articles, many=True).data
    return {
        'current': current,
        'size': size,
        'list': articles,
        'total': total_count,
    }


def blog_timeline_get_article_list(current, size):
    """
    时间轴
    """
    offset = (current - 1) * size
    articles = Article.objects.filter(status=1).order_by('-createdAt')[offset:offset + size]
    total_count = Article.objects.filter(status=1).count()

    result_list = {}
    for article in articles:
        year = f"year_{article.createdAt.year}"
        if year not in result_list:
            result_list[year] = []
        result_list[year].append(article)

    final = [{'year': key.replace('year_', ''), 'articleList': value} for key, value in result_list.items()]

    return {
        'current': current,
        'size': size,
        'list': final,
        'total': total_count,
    }


def get_article_list_by_tag_id(current, size, tag_id):
    """
    通过tagId获取文章列表
    """
    tag_id_list = get_article_id_list_by_tag_id(tag_id)
    offset = (current - 1) * size

    articles = Article.objects.filter(id__in=tag_id_list, status=1).order_by('-createdAt')[offset:offset + size]
    total_count = Article.objects.filter(id__in=tag_id_list, status=1).count()
    articles = ArticleSerializer(articles, many=True).data

    return {
        'current': current,
        'size': size,
        'list': articles,
        'total': total_count,
    }


def get_article_list_by_category_id(current, size, category_id):
    """
    通过分类id获取文章列表
    """
    offset = (current - 1) * size
    articles = Article.objects.filter(category_id=category_id, status=1).order_by('-createdAt')[offset:offset + size]
    total_count = Article.objects.filter(category_id=category_id, status=1).count()
    articles = ArticleSerializer(articles, many=True).data

    return {
        'current': current,
        'size': size,
        'list': articles,
        'total': total_count,
    }


def get_recommend_article_by_id(article_id):
    """
    根据文章id获取推荐文章
    """
    context_previous = Article.objects.filter(id__lt=article_id, status=1).order_by('-id').first()
    content_next = Article.objects.filter(id__gt=article_id, status=1).order_by('id').first()

    if not context_previous:
        context_previous = Article.objects.get(pk=article_id)
    if not content_next:
        content_next = Article.objects.get(pk=article_id)

    tag_id_list = get_tag_list_by_article_id(article_id)
    article_id_list = get_article_id_list_by_tag_id(tag_id_list)

    recommend = Article.objects.filter(id__in=article_id_list, status=1).order_by('-createdAt')[:6]

    return {
        'previous': context_previous,
        'next': content_next,
        'recommend': recommend,
    }


def get_article_count():
    """
    获取文章总数
    """
    return Article.objects.filter(status=1).count()


def get_article_list_by_content(content):
    """
    根据文章内容搜索文章
    """
    articles = Article.objects.filter(article_content__icontains=content, status=1).order_by('-view_times')[:8]
    result = []
    for article in articles:
        index = article.article_content.find(content)
        previous = max(0, index - 12)
        next = index + len(content) + 12
        result.append({
            'id': article.id,
            'article_content': article.article_content[previous:next],
            'article_title': article.article_title,
        })
    return result


def get_hot_article():
    """
    获取热门文章
    """
    return Article.objects.filter(status=1).order_by('-view_times')[:5]


def article_like(article_id):
    """
    文章点赞
    """
    article = Article.objects.get(pk=article_id)
    if article:
        article.increment('thumbs_up_times', by=1)
        return True
    return False


def cancel_article_like(article_id):
    """
    取消文章点赞
    """
    article = Article.objects.get(pk=article_id)
    if article:
        article.decrement('thumbs_up_times', by=1)
        return True
    return False


def add_reading_duration(article_id, duration):
    """
    文章增加阅读时长
    """
    try:
        article = Article.objects.get(pk=article_id)
        article.increment('reading_duration', by=duration)
        return True
    except Article.DoesNotExist:
        return False


def get_article_cover_by_id(article_id):
    """
    根据文章获取文章封面
    """
    article = Article.objects.get(pk=article_id)
    return article.article_cover if article else None


def verify_article_param(request):
    article_title = request.data.get('article_title')
    author_id = request.data.get('author_id')
    category = request.data.get('category')
    article_content = request.data.get('article_content')
    tag_list = request.data.get('tagList')

    if not category:
        return Response(throw_error(error_code, "文章分类必传"), status=400)

    category_name = category.get('category_name')
    if not article_title or not author_id or not category_name or not article_content:
        return Response(throw_error(error_code, "文章参数校验错误"), status=400)

    if not tag_list:
        return Response(throw_error(error_code, "文章标签不能为空"), status=400)

    return None


def create_judge_title_exist(request):
    article_title = request.data.get('article_title')
    res = get_article_info_by_title({'article_title': article_title})
    if res:
        return Response(throw_error(error_code, "已存在相同的文章标题"), status=400)

    return None


def update_judge_title_exist(request):
    id = request.data.get('id')
    article_title = request.data.get('article_title')
    res = get_article_info_by_title({'id': id, 'article_title': article_title})
    if res:
        return Response(throw_error(error_code, "已存在相同的文章标题"), status=400)

    return None


def verify_top_param(id, is_top):
    if not id.isdigit() or not is_top.isdigit():
        return Response(throw_error(error_code, "参数只能为数字"), status=400)

    return None


def verify_del_param(id, status):
    if not id.isdigit() or not status.isdigit():
        return Response(throw_error(error_code, "参数只能为数字"), status=400)

    return None
