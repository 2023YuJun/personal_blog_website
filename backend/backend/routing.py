from django.urls import re_path
from utils.websocket import ChatConsumer  # 替换为您的消费者

websocket_urlpatterns = [
    re_path(r'ws/chat/$', ChatConsumer.as_asgi()),  # 根据需要定义路由
]
