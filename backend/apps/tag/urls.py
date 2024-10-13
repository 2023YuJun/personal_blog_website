from django.urls import path
from .views import TagView
urlpatterns = [
    path('tag/add/', TagView.as_view(), name='add_tag'),
    path('tag/update/', TagView.as_view(), name='update_tag'),
    path('tag/delete/', TagView.as_view(), name='delete_tags'),
    path('tag/getTagList/', TagView.as_view(), name='get_tag_list'),
    path('tag/getTagDictionary/', TagView.as_view(), name='get_tag_dictionary'),
]
