from django.urls import path
from .views import CommentView

urlpatterns = [
    path('comment/add/', CommentView.as_view(), name='add_comment'),
    path('comment/apply/', CommentView.as_view(), name='apply_comment'),
    path('comment/thumbUp/<int:id>/', CommentView.as_view(), name='comment_like'),
    path('comment/cancelCommentLike/<int:id>/', CommentView.as_view(), name='cancel_comment_like'),
    path('comment/delete/<int:id>/<int:parent_id>/', CommentView.as_view(), name='delete_comment'),
    path('comment/backDelete/<int:id>/<int:parent_id>/', CommentView.as_view(), name='back_delete_comment'),
    path('comment/backGetCommentList/', CommentView.as_view(), name='back_get_comment_list'),
    path('comment/frontGetParentComment/', CommentView.as_view(), name='front_get_parent_comment'),
    path('comment/frontGetChildrenComment/', CommentView.as_view(), name='front_get_children_comment'),
    path('comment/getCommentTotal/', CommentView.as_view(), name='get_comment_total'),
]
