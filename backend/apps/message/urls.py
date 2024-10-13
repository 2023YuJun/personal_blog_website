from django.urls import path
from .views import MessageView

urlpatterns = [
    path('message/add/', MessageView.as_view(), name='add_message'),
    path('message/update/', MessageView.as_view(), name='update_message'),
    path('message/delete/', MessageView.as_view(), name='delete_message'),
    path('message/backDelete/', MessageView.as_view(), name='back_delete_message'),
    path('message/like/<int:id>/', MessageView.as_view(), name='message_like'),
    path('message/cancelLike/<int:id>/', MessageView.as_view(), name='cancel_message_like'),
    path('message/getMessageList/', MessageView.as_view(), name='get_message_list'),
    path('message/getAllMessage/', MessageView.as_view(), name='get_all_message'),
    path('message/getHotTagList/', MessageView.as_view(), name='get_hot_tag_list'),
]
