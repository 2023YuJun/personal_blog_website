from django.urls import path
from .views import TalkView
urlpatterns = [
    path('talk/publishTalk/', TalkView.as_view(), name='publish_talk'),
    path('talk/updateTalk/', TalkView.as_view(), name='update_talk'),
    path('talk/deleteTalkById/<int:id>/<int:status>/', TalkView.as_view(), name='delete_talk_by_id'),
    path('talk/togglePublic/<int:id>/<int:status>/', TalkView.as_view(), name='toggle_public'),
    path('talk/toggleTop/<int:id>/<int:is_top>/', TalkView.as_view(), name='toggle_top'),
    path('talk/revertTalk/<int:id>/', TalkView.as_view(), name='revert_talk'),
    path('talk/getTalkList/', TalkView.as_view(), name='get_talk_list'),
    path('talk/getTalkById/<int:id>/', TalkView.as_view(), name='get_talk_by_id'),
    path('talk/like/<int:id>/', TalkView.as_view(), name='talk_like'),
    path('talk/cancelLike/<int:id>/', TalkView.as_view(), name='cancel_talk_like'),
    path('talk/blogGetTalkList/', TalkView.as_view(), name='blog_get_talk_list'),
]
