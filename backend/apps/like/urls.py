from django.urls import path
from .views import LikeView

urlpatterns = [
    path('like/addLike/', LikeView.as_view(), name='add_like'),
    path('like/cancelLike/', LikeView.as_view(), name='cancel_like'),
    path('like/getIsLikeByIdOrIpAndType/', LikeView.as_view(), name='get_is_like_by_id_or_ip_and_type'),
]
