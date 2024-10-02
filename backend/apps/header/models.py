from django.db import models


class Header(models.Model):
    bg_url = models.CharField(max_length=255, null=True, blank=True, verbose_name='背景图')
    createdAt = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    updatedAt = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')
    route_name = models.CharField(max_length=555, null=True, blank=True, verbose_name='路由名称')

    class Meta:
        db_table = 'blog_header'

    def __str__(self):
        return self.route_name if self.route_name else '无路由'
