from rest_framework import serializers
from .models import Notify


class NotifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Notify
        fields = '__all__'
