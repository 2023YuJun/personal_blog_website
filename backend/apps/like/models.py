from django.db import models


class Like(models.Model):
    LIKE_TYPE_CHOICES = [
        (1, '文章'),
        (2, '说说'),
        (3, '留言'),
        (4, '评论'),
    ]

    type = models.IntegerField(choices=LIKE_TYPE_CHOICES, null=True, blank=True, verbose_name='点赞类型')
    for_id = models.IntegerField(null=True, blank=True, verbose_name='点赞id 文章id 说说id 留言id')
    user_id = models.IntegerField(null=True, blank=True, verbose_name='点赞用户id')
    createdAt = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    updatedAt = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')
    ip = models.CharField(max_length=255, null=True, blank=True, verbose_name='点赞IP')

    class Meta:
        db_table = 'blog_like'

    def __str__(self):
        return f'点赞类型: {self.get_type_display()}, 用户ID: {self.user_id}'
