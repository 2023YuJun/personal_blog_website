from rest_framework import serializers
from .models import Message
from apps.user.service import get_one_user_info
from apps.like.service import get_is_like_by_ip_and_type, get_is_like_by_id_and_type
from apps.comment.service import get_comment_total


class MessageSerializer(serializers.ModelSerializer):
    createdAt = serializers.SerializerMethodField()
    updatedAt = serializers.SerializerMethodField()
    nick_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    comment_total = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = '__all__'

    def get_createdAt(self, obj):
        return obj.createdAt.strftime('%Y-%m-%d %H:%M:%S')

    def get_updatedAt(self, obj):
        return obj.updatedAt.strftime('%Y-%m-%d %H:%M:%S')

    def get_nick_name(self, obj):
        if obj.user_id:
            user_info = get_one_user_info({"id": obj.user_id})
            obj.nick_name = user_info.nick_name
        else:
            obj.nick_name = ''
        return obj.nick_name

    def get_avatar(self, obj):
        if obj.user_id:
            user_info = get_one_user_info({"id": obj.user_id})
            obj.avatar = user_info.avatar
        else:
            obj.avatar = ''
        return obj.avatar

    def get_is_like(self, obj):
        user_id = self.context.get('user_id', None)
        ip = self.context.get('ip', None)
        if user_id:
            return get_is_like_by_id_and_type(obj.id, 3, user_id)
        else:
            return get_is_like_by_ip_and_type(obj.id, 3, ip)

    def get_comment_total(self, obj):
        return get_comment_total(obj.id, 3)
