from rest_framework import serializers
from .models import Talk
from .models import TalkPhoto
from ..user.service import get_one_user_info
from django.utils import timezone


class TalkSerializer(serializers.ModelSerializer):
    talkImgList = serializers.SerializerMethodField()
    nick_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    createdAt = serializers.SerializerMethodField()
    updatedAt = serializers.SerializerMethodField()

    class Meta:
        model = Talk
        fields = '__all__'

    def get_talkImgList(self, obj):
        from .talkPhoto_service import get_photo_by_talk_id
        # 从图片模型获取图片列表
        photos = get_photo_by_talk_id(obj.id)
        return [photo['url'] for photo in photos] if photos else []

    def get_nick_name(self, obj):
        # 从用户模型获取用户的昵称
        user_info = get_one_user_info({'id': obj.user_id})
        return user_info.nick_name if user_info else None

    def get_avatar(self, obj):
        # 从用户模型获取用户的头像
        user_info = get_one_user_info({'id': obj.user_id})
        return user_info.avatar if user_info else None

    def get_createdAt(self, obj):
        local_time = timezone.localtime(obj.createdAt)
        return local_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_updatedAt(self, obj):
        local_time = timezone.localtime(obj.updatedAt)
        return local_time.strftime('%Y-%m-%d %H:%M:%S')


class TalkPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalkPhoto
        fields = '__all__'
