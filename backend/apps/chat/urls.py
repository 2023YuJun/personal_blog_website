from django.urls import path
from .views import ChatView

urlpatterns = [
    path('chat/create/', ChatView.as_view(), name='create_chat'),  # 新增聊天
    path('chat/delete/', ChatView.as_view(), name='delete_chats'),  # 删除聊天
    path('chat/deleteOne/<int:id>/', ChatView.as_view(), name='delete_one_chat'),  # 删除单条聊天
    path('chat/getChatList/', ChatView.as_view(), name='get_chat_list'),  # 条件分页查找聊天列表
]
