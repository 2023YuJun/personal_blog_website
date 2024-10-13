from django.urls import path
from .views import LinksView

urlpatterns = [
    path('links/add/', LinksView.as_view(), name='add_or_update_links'),
    path('links/frontUpdate/', LinksView.as_view(), name='front_update_links'),
    path('links/backUpdate/', LinksView.as_view(), name='back_update_links'),
    path('links/delete/', LinksView.as_view(), name='delete_links'),
    path('links/approve/', LinksView.as_view(), name='approve_links'),
    path('links/getLinksList/', LinksView.as_view(), name='get_links_list'),
]
