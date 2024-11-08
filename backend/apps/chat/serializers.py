from rest_framework import serializers
from .models import Chat
from apps.user.service import get_one_user_info


class ChatSerializer(serializers.ModelSerializer):
    nick_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    createdAt = serializers.SerializerMethodField()
    updatedAt = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = '__all__'

    def get_nick_name(self, obj):
        if obj.user_id:
            user = get_one_user_info({'id': obj.user_id})
            return user.nick_name if user else None
        return None

    def get_avatar(self, obj):
        if obj.user_id:
            user = get_one_user_info({'id': obj.user_id})
            return user.avatar if user else None
        return None

    def get_createdAt(self, obj):
        return obj.createdAt.strftime('%Y-%m-%d %H:%M:%S')

    def get_updatedAt(self, obj):
        return obj.updatedAt.strftime('%Y-%m-%d %H:%M:%S')
