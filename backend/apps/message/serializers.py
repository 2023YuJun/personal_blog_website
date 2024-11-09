from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    createdAt = serializers.SerializerMethodField()
    updatedAt = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = '__all__'

    def get_createdAt(self, obj):
        return obj.createdAt.strftime('%Y-%m-%d %H:%M:%S')

    def get_updatedAt(self, obj):
        return obj.updatedAt.strftime('%Y-%m-%d %H:%M:%S')
