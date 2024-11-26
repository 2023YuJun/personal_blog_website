from rest_framework import serializers
from .models import Article
from .models import ArticleTag
from django.utils import timezone
from apps.category.service import get_category_name_by_id
from apps.article.articleTag_service import get_tag_list_by_article_id
from apps.user.service import get_author_name_by_id


class ArticleSerializer(serializers.ModelSerializer):
    categoryName = serializers.SerializerMethodField()
    tagNameList = serializers.SerializerMethodField()
    tagIdList = serializers.SerializerMethodField()
    authorName = serializers.SerializerMethodField()
    createdAt = serializers.SerializerMethodField()
    updatedAt = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'

    def get_categoryName(self, obj):
        return get_category_name_by_id(obj.category_id) if obj.category_id else None

    def get_tagNameList(self, obj):
        return get_tag_list_by_article_id(obj.id).get('tag_name_list', []) if obj.id else None

    def get_tagIdList(self, obj):
        return get_tag_list_by_article_id(obj.id).get('tag_id_list', [])

    def get_authorName(self, obj):
        return get_author_name_by_id(obj.author_id)

    def get_createdAt(self, obj):
        local_time = timezone.localtime(obj.createdAt)
        return local_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_updatedAt(self, obj):
        local_time = timezone.localtime(obj.updatedAt)
        return local_time.strftime('%Y-%m-%d %H:%M:%S')


class ArticleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleTag
        fields = '__all__'

