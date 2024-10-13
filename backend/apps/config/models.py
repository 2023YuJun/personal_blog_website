from django.db import models


class Config(models.Model):
    blog_name = models.CharField(max_length=55, null=True, default='范同学的博客', verbose_name='博客名称')
    blog_avatar = models.CharField(max_length=255, null=True, default='https://mrzym.gitee.io/blogimg/html/rabbit.png',
                                   verbose_name='博客头像')
    avatar_bg = models.CharField(max_length=255, null=True, blank=True, verbose_name='博客头像背景图')
    personal_say = models.CharField(max_length=255, null=True, blank=True, verbose_name='个人签名')
    blog_notice = models.CharField(max_length=255, null=True, blank=True, verbose_name='博客公告')
    qq_link = models.CharField(max_length=255, null=True, blank=True, verbose_name='QQ链接')
    we_chat_link = models.CharField(max_length=255, null=True, blank=True, verbose_name='微信链接')
    github_link = models.CharField(max_length=255, null=True, blank=True, verbose_name='GitHub链接')
    git_ee_link = models.CharField(max_length=255, null=True, blank=True, verbose_name='Git EE链接')
    bilibili_link = models.CharField(max_length=255, null=True, blank=True, verbose_name='Bilibili链接')
    view_time = models.BigIntegerField(default=0, null=True, verbose_name='博客被访问的次数')
    createdAt = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    updatedAt = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')
    we_chat_group = models.CharField(max_length=255, null=True, blank=True, verbose_name='微信群图片')
    qq_group = models.CharField(max_length=255, null=True, blank=True, verbose_name='QQ群图片')
    we_chat_pay = models.CharField(max_length=255, null=True, blank=True, verbose_name='微信收款码')
    ali_pay = models.CharField(max_length=255, null=True, blank=True, verbose_name='支付宝收款码')

    class Meta:
        db_table = 'blog_config'

    def __str__(self):
        return self.blog_name
