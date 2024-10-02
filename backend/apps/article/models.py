from django.db import models


class Article(models.Model):
    ARTICLE_TYPE_CHOICES = [
        (1, '原创'),
        (2, '转载'),
        (3, '翻译'),
    ]
    ARTICLE_STATUS_CHOICES = [
        (1, '公开'),
        (2, '私密'),
        (3, '草稿箱'),
    ]
    IS_TOP_CHOICES = [
        (1, '置顶'),
        (2, '取消置顶'),
    ]

    article_title = models.CharField(max_length=255, verbose_name='文章标题')
    author_id = models.IntegerField(default=1, verbose_name='文章作者')
    category_id = models.IntegerField(null=True, verbose_name='分类id')
    article_content = models.TextField(blank=True, verbose_name='文章内容')
    article_cover = models.CharField(max_length=1234, default='https://mrzym.gitee.io/blogimg/html/rabbit.png',
                                     verbose_name='文章缩略图')
    is_top = models.IntegerField(default=2, choices=IS_TOP_CHOICES, verbose_name='是否置顶')
    status = models.IntegerField(default=1, choices=ARTICLE_STATUS_CHOICES, verbose_name='文章状态')
    type = models.IntegerField(default=1, choices=ARTICLE_TYPE_CHOICES, verbose_name='文章类型')
    origin_url = models.CharField(max_length=255, null=True, blank=True, verbose_name='原文链接')
    createdAt = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    updatedAt = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')
    view_times = models.IntegerField(default=0, verbose_name='文章访问次数')
    article_description = models.CharField(max_length=255, verbose_name='描述信息')
    thumbs_up_times = models.IntegerField(default=0, verbose_name='文章点赞次数')
    reading_duration = models.FloatField(default=0, verbose_name='文章阅读时长')
    order = models.IntegerField(null=True, blank=True, verbose_name='排序')

    class Meta:
        db_table = 'blog_article'


class ArticleTag(models.Model):
    article_id = models.IntegerField(null=True, verbose_name='文章id')
    tag_id = models.IntegerField(null=True, verbose_name='标签id')
    createdAt = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    updatedAt = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')

    class Meta:
        db_table = 'blog_article_tag'
