from django.db import transaction
from django.db.models import Q
from ..models import Article
from articleTag import article_tag_service
from ...category.service.category import category_service
from ...user.service.user import user_service


class ArticleService:
    """
    文章服务类
    """

    async def update_url(self):
        """
        批量替换url
        """
        articles = await Article.objects.all()
        for article in articles:
            article.article_cover = article.article_cover.replace("http://img.mrzym.top/", "http://mrzym.top/online/")
            await article.save()

    async def create_article(self, article_data):
        """
        新增文章
        """
        try:
            with transaction.atomic():
                article = Article(**article_data)
                await article.save()
                return article
        except Exception as e:
            print(e)
            return None

    async def update_article(self, article_data):
        """
        修改文章信息
        """
        try:
            article = await Article.objects.get(pk=article_data['id'])
            for attr, value in article_data.items():
                setattr(article, attr, value)
            await article.save()
            return True
        except Article.DoesNotExist:
            return False
        except Exception as e:
            print(e)
            return False

    async def update_top(self, article_id, is_top):
        """
        修改文章置顶信息
        """
        return await Article.objects.filter(id=article_id).update(is_top=is_top) > 0

    async def delete_article(self, article_id, status):
        """
        删除文章
        """
        if status != 3:
            return await Article.objects.filter(id=article_id).update(status=3) > 0
        else:
            async with transaction.atomic():
                await article_tag_service.delete_article_tag(article_id)
                return await Article.objects.filter(id=article_id).delete() > 0

    async def revert_article(self, article_id):
        """
        恢复文章
        """
        return await Article.objects.filter(id=article_id).update(status=1) > 0

    async def toggle_article_public(self, article_id, status):
        """
        公开或隐藏文章
        """
        new_status = 1 if status == 2 else 2
        return await Article.objects.filter(id=article_id).update(status=new_status) > 0

    async def get_article_info_by_title(self, title, article_id=None):
        """
        根据文章标题获取文章信息
        """
        article = await Article.objects.filter(article_title=title).first()
        if article:
            return article.id != article_id if article_id else True
        return False

    async def get_article_list(self, params):
        """
        条件分页查询文章列表
        """
        current = params.get('current', 1)
        size = params.get('size', 10)
        offset = (current - 1) * size

        query = Q(status__in=[1, 2])
        if 'article_title' in params:
            query &= Q(article_title__icontains=params['article_title'])
        if 'is_top' in params:
            query &= Q(is_top=params['is_top'])
        if 'category_id' in params:
            query &= Q(category_id=params['category_id'])
        if 'create_time' in params:
            query &= Q(createdAt__range=params['create_time'])

        articles = await Article.objects.filter(query).exclude(article_content=None).order_by('-createdAt')[offset:offset + size]
        total_count = await Article.objects.filter(query).count()

        for article in articles:
            article.category_name = await category_service.get_category_name_by_id(article.category_id)
            article.tag_name_list = await article_tag_service.get_tag_list_by_article_id(article.id)

        return {
            'current': current,
            'size': size,
            'list': articles,
            'total': total_count,
        }

    async def get_article_by_id(self, article_id):
        """
        根据文章id获取文章详细信息
        """
        article = await Article.objects.get(pk=article_id)
        if article:
            await article.increment('view_times', by=1)
            article.tag_id_list = await article_tag_service.get_tag_list_by_article_id(article_id)
            article.category_name = await category_service.get_category_name_by_id(article.category_id)
            article.author_name = await user_service.get_author_name_by_id(article.author_id)
            return article
        return None

    async def blog_home_get_article_list(self, current, size):
        """
        博客前台获取文章列表
        """
        offset = (current - 1) * size
        articles = await Article.objects.filter(status=1).order_by('is_top', 'order', '-createdAt')[offset:offset + size]
        total_count = await Article.objects.filter(status=1).count()

        for article in articles:
            article.category_name = await category_service.get_category_name_by_id(article.category_id)
            article.tag_name_list = await article_tag_service.get_tag_list_by_article_id(article.id)

        return {
            'current': current,
            'size': size,
            'list': articles,
            'total': total_count,
        }

    async def blog_timeline_get_article_list(self, current, size):
        """
        时间轴
        """
        offset = (current - 1) * size
        articles = await Article.objects.filter(status=1).order_by('-createdAt')[offset:offset + size]
        total_count = await Article.objects.filter(status=1).count()

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

    async def get_article_list_by_tag_id(self, current, size, tag_id):
        """
        通过tagId获取文章列表
        """
        tag_id_list = await article_tag_service.get_article_id_list_by_tag_id(tag_id)
        offset = (current - 1) * size

        articles = await Article.objects.filter(id__in=tag_id_list, status=1).order_by('-createdAt')[offset:offset + size]
        total_count = await Article.objects.filter(id__in=tag_id_list, status=1).count()

        return {
            'current': current,
            'size': size,
            'list': articles,
            'total': total_count,
        }

    async def get_article_list_by_category_id(self, current, size, category_id):
        """
        通过分类id获取文章列表
        """
        offset = (current - 1) * size
        articles = await Article.objects.filter(category_id=category_id, status=1).order_by('-createdAt')[offset:offset + size]
        total_count = await Article.objects.filter(category_id=category_id, status=1).count()

        return {
            'current': current,
            'size': size,
            'list': articles,
            'total': total_count,
        }

    async def get_recommend_article_by_id(self, article_id):
        """
        根据文章id获取推荐文章
        """
        context_previous = await Article.objects.filter(id__lt=article_id, status=1).order_by('-id').first()
        content_next = await Article.objects.filter(id__gt=article_id, status=1).order_by('id').first()

        if not context_previous:
            context_previous = await Article.objects.get(pk=article_id)
        if not content_next:
            content_next = await Article.objects.get(pk=article_id)

        tag_id_list = await article_tag_service.get_tag_list_by_article_id(article_id)
        article_id_list = await article_tag_service.get_article_id_list_by_tag_id(tag_id_list)

        recommend = await Article.objects.filter(id__in=article_id_list, status=1).order_by('-createdAt')[:6]

        return {
            'previous': context_previous,
            'next': content_next,
            'recommend': recommend,
        }

    async def get_article_count(self):
        """
        获取文章总数
        """
        return await Article.objects.filter(status=1).count()

    async def get_article_list_by_content(self, content):
        """
        根据文章内容搜索文章
        """
        articles = await Article.objects.filter(article_content__icontains=content, status=1).order_by('-view_times')[:8]
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

    async def get_hot_article(self):
        """
        获取热门文章
        """
        return await Article.objects.filter(status=1).order_by('-view_times')[:5]

    async def article_like(self, article_id):
        """
        文章点赞
        """
        article = await Article.objects.get(pk=article_id)
        if article:
            await article.increment('thumbs_up_times', by=1)
            return True
        return False

    async def cancel_article_like(self, article_id):
        """
        取消文章点赞
        """
        article = await Article.objects.get(pk=article_id)
        if article:
            await article.decrement('thumbs_up_times', by=1)
            return True
        return False

    async def add_reading_duration(self, article_id, duration):
        """
        文章增加阅读时长
        """
        try:
            article = await Article.objects.get(pk=article_id)
            await article.increment('reading_duration', by=duration)
            return True
        except Article.DoesNotExist:
            return False

    async def get_article_cover_by_id(self, article_id):
        """
        根据文章获取文章封面
        """
        article = await Article.objects.get(pk=article_id)
        return article.article_cover if article else None


# 创建服务实例
article_service = ArticleService()
