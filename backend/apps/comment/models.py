from django.db import models


class Comment(models.Model):
    parent_id = models.IntegerField(null=True, blank=True, verbose_name='评论父级id')
    for_id = models.IntegerField(null=True, blank=True, verbose_name='评论的对象id')
    type = models.IntegerField(null=True, blank=True, verbose_name='评论类型')
    from_id = models.IntegerField(null=True, blank=True, verbose_name='评论人id')
    from_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='评论人昵称')
    from_avatar = models.CharField(max_length=555, null=True, blank=True, verbose_name='评论人头像')
    to_id = models.IntegerField(null=True, blank=True, verbose_name='被回复的人id')
    to_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='被回复人的昵称')
    to_avatar = models.CharField(max_length=555, null=True, blank=True, verbose_name='被回复人的头像')
    content = models.TextField(null=True, blank=True, verbose_name='评论内容')
    thumbs_up = models.IntegerField(default=0, verbose_name='评论点赞数')
    createdAt = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    updatedAt = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')
    ip = models.CharField(max_length=255, null=True, blank=True, verbose_name='ip地址')

    class Meta:
        db_table = 'blog_comment'

    def __str__(self):
        return f'评论者: {self.from_name}, 内容: {self.content}'
