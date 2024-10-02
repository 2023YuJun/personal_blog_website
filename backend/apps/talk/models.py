from django.db import models


class Talk(models.Model):
    user_id = models.IntegerField(null=True, blank=True, verbose_name='发布说说的用户ID')
    content = models.CharField(max_length=255, null=True, blank=True, verbose_name='说说内容')
    status = models.IntegerField(default=1, null=True, blank=True, verbose_name='说说状态')
    is_top = models.IntegerField(default=2, null=True, blank=True, verbose_name='是否置顶')
    like_times = models.IntegerField(default=0, null=True, blank=True, verbose_name='点赞次数')
    createdAt = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    updatedAt = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')

    class Meta:
        db_table = 'blog_talk'

    def __str__(self):
        return self.content if self.content else '无说说内容'


class TalkPhoto(models.Model):
    talk_id = models.IntegerField(null=True, blank=True, verbose_name='说说的ID')
    url = models.CharField(max_length=255, null=True, blank=True, verbose_name='图片地址')
    createdAt = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    updatedAt = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')

    class Meta:
        db_table = 'blog_talk_photo'

    def __str__(self):
        return self.url if self.url else '无图片地址'
