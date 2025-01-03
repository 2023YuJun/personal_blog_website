# Generated by Django 5.1.1 on 2024-10-06 07:10

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Article",
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
                    "article_title",
                    models.CharField(max_length=255, verbose_name="文章标题"),
                ),
                ("author_id", models.IntegerField(default=1, verbose_name="文章作者")),
                ("category_id", models.IntegerField(null=True, verbose_name="分类id")),
                ("article_content", models.TextField(blank=True, verbose_name="文章内容")),
                (
                    "article_cover",
                    models.CharField(
                        default="https://mrzym.gitee.io/blogimg/html/rabbit.png",
                        max_length=1234,
                        verbose_name="文章缩略图",
                    ),
                ),
                (
                    "is_top",
                    models.IntegerField(
                        choices=[(1, "置顶"), (2, "取消置顶")], default=2, verbose_name="是否置顶"
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[(1, "公开"), (2, "私密"), (3, "草稿箱")],
                        default=1,
                        verbose_name="文章状态",
                    ),
                ),
                (
                    "type",
                    models.IntegerField(
                        choices=[(1, "原创"), (2, "转载"), (3, "翻译")],
                        default=1,
                        verbose_name="文章类型",
                    ),
                ),
                (
                    "origin_url",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="原文链接"
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
                ("view_times", models.IntegerField(default=0, verbose_name="文章访问次数")),
                (
                    "article_description",
                    models.CharField(max_length=255, verbose_name="描述信息"),
                ),
                (
                    "thumbs_up_times",
                    models.IntegerField(default=0, verbose_name="文章点赞次数"),
                ),
                (
                    "reading_duration",
                    models.FloatField(default=0, verbose_name="文章阅读时长"),
                ),
                (
                    "order",
                    models.IntegerField(blank=True, null=True, verbose_name="排序"),
                ),
            ],
            options={
                "db_table": "blog_article",
            },
        ),
        migrations.CreateModel(
            name="ArticleTag",
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
                ("article_id", models.IntegerField(null=True, verbose_name="文章id")),
                ("tag_id", models.IntegerField(null=True, verbose_name="标签id")),
                (
                    "createdAt",
                    models.DateTimeField(blank=True, null=True, verbose_name="创建时间"),
                ),
                (
                    "updatedAt",
                    models.DateTimeField(blank=True, null=True, verbose_name="更新时间"),
                ),
            ],
            options={
                "db_table": "blog_article_tag",
            },
        ),
    ]
