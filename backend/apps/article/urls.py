from django.urls import path
from .views import ArticleView

urlpatterns = [
    path('article/add/', ArticleView.as_view(), name='create_article'),
    path('article/update/', ArticleView.as_view(), name='update_article'),
    path('article/updateTop/<int:id>/<int:is_top>/',  ArticleView.as_view(), name='update_top'),
    path('article/delete/<int:id>/<int:status>/', ArticleView.as_view(), name='delete_article'),
    path('article/revert/<int:id>/', ArticleView.as_view(), name='revert_article'),
    path('article/isPublic/<int:id>/<int:status>/', ArticleView.as_view(), name='toggle_article_public'),
    path('article/titleExist/', ArticleView.as_view(), name='get_article_info_by_title'),
    path('article/getArticleList/', ArticleView.as_view(), name='get_article_list'),
    path('article/blogHomeGetArticleList/<int:current>/<int:size>/', ArticleView.as_view(), name='blog_home_get_article_list'),
    path('article/blogTimelineGetArticleList/<int:current>/<int:size>/', ArticleView.as_view(),
         name='blog_timeline_get_article_list'),
    path('article/getArticleListByTagId/', ArticleView.as_view(), name='get_article_list_by_tag_id'),
    path('article/getArticleListByCategoryId/', ArticleView.as_view(),
         name='get_article_list_by_category_id'),
    path('article/getRecommendArticleById/<int:id>/', ArticleView.as_view(), name='get_recommend_article_by_id'),
    path('article/getArticleById/<int:id>/', ArticleView.as_view(), name='get_article_by_id'),
    path('article/getHotArticle/', ArticleView.as_view(), name='get_hot_article'),
    path('article/getArticleListByContent/<str:content>/', ArticleView.as_view(), name='get_article_list_by_content'),
    path('article/addReadingDuration/<int:id>/<int:duration>/', ArticleView.as_view(), name='add_reading_duration')
]
