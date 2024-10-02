from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name='账号名唯一')
    password = models.CharField(max_length=64, verbose_name='密码')
    role = models.IntegerField(default=2, verbose_name='用户角色')
    nick_name = models.CharField(max_length=255, default='', verbose_name='用户昵称')
    avatar = models.CharField(max_length=255, default='', verbose_name='用户头像')
    createdAt = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    updatedAt = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')
    email = models.EmailField(max_length=255, null=True, blank=True, verbose_name='邮箱')
    phone = models.CharField(max_length=255, null=True, blank=True, verbose_name='手机号')
    qq = models.CharField(max_length=255, default='', verbose_name='用户QQ，用于联系')
    ip = models.CharField(max_length=255, default='', verbose_name='IP属地')

    class Meta:
        db_table = 'blog_user'

