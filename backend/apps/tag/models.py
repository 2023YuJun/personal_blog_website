from django.db import models


class Tag(models.Model):
    tag_name = models.CharField(max_length=55, unique=True, null=True, blank=True, verbose_name='标签名称')
    createdAt = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    updatedAt = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')

    class Meta:
        db_table = 'blog_tag'

    def __str__(self):
        return self.tag_name if self.tag_name else '无标签名称'
