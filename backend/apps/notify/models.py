from django.db import models


class Notify(models.Model):
    NOTIFY_TYPE_CHOICES = [
        (1, '文章'),
        (2, '说说'),
        (3, '留言'),
        (4, '友链'),
    ]

    message = models.CharField(max_length=555, null=True, blank=True, verbose_name='通知内容')
    user_id = models.IntegerField(null=True, blank=True, verbose_name='通知给谁')
    type = models.IntegerField(choices=NOTIFY_TYPE_CHOICES, null=True, blank=True, verbose_name='通知类型')
    to_id = models.IntegerField(null=True, blank=True, verbose_name='目标ID')
    isView = models.IntegerField(default=1, null=True, blank=True, verbose_name='是否被查看')
    createdAt = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    updatedAt = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')

    class Meta:
        db_table = 'blog_notify'

    def __str__(self):
        return f'通知内容: {self.message if self.message else "无内容"}'
