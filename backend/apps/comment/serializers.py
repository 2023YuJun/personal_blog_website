from rest_framework import serializers
from .models import Comment
from django.utils import timezone


class CommentSerializer(serializers.ModelSerializer):
    createdAt = serializers.SerializerMethodField()
    updatedAt = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_createdAt(self, obj):
        local_time = timezone.localtime(obj.createdAt)
        return local_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_updatedAt(self, obj):
        local_time = timezone.localtime(obj.updatedAt)
        return local_time.strftime('%Y-%m-%d %H:%M:%S')
