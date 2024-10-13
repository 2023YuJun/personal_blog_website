from rest_framework import serializers
from .models import Config


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = '__all__'  # 你可以根据需要列出具体的字段
