# Generated by Django 5.1.1 on 2024-10-06 07:10

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Links",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "site_name",
                    models.CharField(
                        blank=True, max_length=55, null=True, verbose_name="网站名称"
                    ),
                ),
                (
                    "site_desc",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="网站描述"
                    ),
                ),
                (
                    "site_avatar",
                    models.CharField(
                        blank=True, max_length=555, null=True, verbose_name="网站头像"
                    ),
                ),
                (
                    "url",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="网站地址"
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        blank=True,
                        choices=[(1, "待审核"), (2, "审核通过")],
                        null=True,
                        verbose_name="友链状态",
                    ),
                ),
                (
                    "createdAt",
                    models.DateTimeField(blank=True, null=True, verbose_name="创建时间"),
                ),
                (
                    "updatedAt",
                    models.DateTimeField(blank=True, null=True, verbose_name="更新时间"),
                ),
                (
                    "user_id",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="申请者id"
                    ),
                ),
            ],
            options={
                "db_table": "blog_links",
            },
        ),
    ]