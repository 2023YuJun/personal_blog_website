from django.db import models


class Chat(models.Model):
    user_id = models.IntegerField(null=True, blank=True, verbose_name='用户id')
    content = models.CharField(max_length=555, null=True, blank=True, verbose_name='聊天内容')
    createdAt = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    updatedAt = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')
    content_type = models.CharField(max_length=55, null=True, blank=True, verbose_name='聊天内容格式')

    class Meta:
        db_table = 'blog_chat'

    def __str__(self):
        return self.content
