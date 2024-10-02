from django.db import models


class Photo(models.Model):
    album_id = models.IntegerField(null=True, blank=True, verbose_name='相册 ID')
    url = models.CharField(max_length=555, null=True, blank=True, verbose_name='图片地址')
    status = models.IntegerField(default=1, null=True, blank=True, verbose_name='状态')
    createdAt = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    updatedAt = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')

    class Meta:
        db_table = 'blog_photo'

    def __str__(self):
        return self.url if self.url else '无图片地址'


class PhotoAlbum(models.Model):
    album_name = models.CharField(max_length=26, null=True, blank=True, verbose_name='相册名称')
    description = models.CharField(max_length=55, null=True, blank=True, verbose_name='相册描述信息')
    createdAt = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    updatedAt = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')
    album_cover = models.CharField(max_length=555, null=True, blank=True, verbose_name='相册封面')

    class Meta:
        db_table = 'blog_photo_album'

    def __str__(self):
        return self.album_name if self.album_name else '无相册名称'
