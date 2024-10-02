from django.db import models


class Recommend(models.Model):
    title = models.CharField(max_length=55, null=True, blank=True, verbose_name='推荐网站标题')
    link = models.CharField(max_length=255, null=True, blank=True, verbose_name='网站地址')
    createdAt = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    updatedAt = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')

    class Meta:
        db_table = 'blog_recommend'

    def __str__(self):
        return self.title if self.title else '无推荐标题'
