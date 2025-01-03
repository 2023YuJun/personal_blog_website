# Generated by Django 5.1.1 on 2024-10-06 07:10

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Chat",
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
                    "user_id",
                    models.IntegerField(blank=True, null=True, verbose_name="用户id"),
                ),
                (
                    "content",
                    models.CharField(
                        blank=True, max_length=555, null=True, verbose_name="聊天内容"
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
                    "content_type",
                    models.CharField(
                        blank=True, max_length=55, null=True, verbose_name="聊天内容格式"
                    ),
                ),
            ],
            options={
                "db_table": "blog_chat",
            },
        ),
    ]
