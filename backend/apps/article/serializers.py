from rest_framework import serializers
from .models import Article  # 根据你的项目结构调整导入路径


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'content',
            'article_cover',
            'is_top',
            'status',
            'created_at',
            'updated_at',
            'reading_duration',
            'likes',
            # 添加其他需要的字段
        ]

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
