from django.db import models


class Links(models.Model):
    STATUS_CHOICES = [
        (1, '待审核'),
        (2, '审核通过'),
    ]

    site_name = models.CharField(max_length=55, null=True, blank=True, verbose_name='网站名称')
    site_desc = models.CharField(max_length=255, null=True, blank=True, verbose_name='网站描述')
    site_avatar = models.CharField(max_length=555, null=True, blank=True, verbose_name='网站头像')
    url = models.CharField(max_length=255, null=True, blank=True, verbose_name='网站地址')
    status = models.IntegerField(choices=STATUS_CHOICES, null=True, blank=True, verbose_name='友链状态')
    createdAt = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    updatedAt = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')
    user_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='申请者id')

    class Meta:
        db_table = 'blog_links'

    def __str__(self):
        return self.site_name if self.site_name else '无网站名称'
