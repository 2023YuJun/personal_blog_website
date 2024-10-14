from rest_framework import serializers
from .models import Notify


class NotifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Notify
        fields = '__all__'  # 你可以根据需要列出具体的字段
