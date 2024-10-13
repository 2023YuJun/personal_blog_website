
from django.urls import path
from .views import CategoryView

urlpatterns = [
    path('category/add/', CategoryView.as_view(), name='add_category'),
    path('category/update/', CategoryView.as_view(), name='update_category'),
    path('category/delete/', CategoryView.as_view(), name='delete_categories'),
    path('category/getCategoryList/', CategoryView.as_view(), name='get_category_list'),
    path('category/getCategoryDictionary/', CategoryView.as_view(), name='get_category_dictionary'),
]