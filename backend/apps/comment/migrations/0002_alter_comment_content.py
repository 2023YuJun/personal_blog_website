# Generated by Django 5.1.1 on 2024-10-27 13:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("comment", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="content",
            field=models.CharField(
                blank=True, max_length=1000, null=True, verbose_name="评论内容"
            ),
        ),
    ]