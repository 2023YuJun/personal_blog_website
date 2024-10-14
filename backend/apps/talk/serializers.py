from rest_framework import serializers
from .models import Talk
from .models import TalkPhoto


class TalkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talk
        fields = '__all__'


class TalkPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalkPhoto
        fields = '__all__'
