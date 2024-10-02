from django.db import models


class Message(models.Model):
    tag = models.CharField(max_length=255, null=True, blank=True, verbose_name='标签')
    message = models.CharField(max_length=555, null=True, blank=True, verbose_name='留言内容')
    color = models.CharField(max_length=255, default='#676767', null=True, blank=True, verbose_name='字体颜色')
    font_size = models.IntegerField(default=12, null=True, blank=True, verbose_name='字体大小')
    bg_color = models.CharField(max_length=255, null=True, blank=True, verbose_name='背景颜色')
    bg_url = models.CharField(max_length=255, null=True, blank=True, verbose_name='背景图片')
    user_id = models.IntegerField(null=True, blank=True, verbose_name='留言用户的id')
    like_times = models.IntegerField(default=0, null=True, blank=True, verbose_name='点赞次数')
    createdAt = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    updatedAt = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')
    font_weight = models.IntegerField(default=500, null=True, blank=True, verbose_name='字体宽度')
    nick_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='游客用户的昵称')

    class Meta:
        db_table = 'blog_message'

    def __str__(self):
        return self.message if self.message else '无留言内容'
