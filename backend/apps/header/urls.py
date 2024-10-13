from django.urls import path
from .views import HeaderView

urlpatterns = [
    path('pageHeader/addOrUpdate/', HeaderView.as_view(), name='add_or_update_header'),
    path('pageHeader/delete/', HeaderView.as_view(), name='delete_header'),
    path('pageHeader/getAll/', HeaderView.as_view(), name='get_all_header'),
]
