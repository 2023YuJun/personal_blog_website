from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=55, unique=True, verbose_name='分类名称')
    createdAt = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    updatedAt = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')

    class Meta:
        db_table = 'blog_category'

    def __str__(self):
        return self.category_name
