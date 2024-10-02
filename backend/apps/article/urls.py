from django.urls import path
from .views import ArticleViewSet

urlpatterns = [
    path('articles/', ArticleViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('articles/<int:pk>/', ArticleViewSet.as_view({'put': 'update', 'delete': 'delete', 'get': 'retrieve'})),
]
