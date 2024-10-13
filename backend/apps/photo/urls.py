from django.urls import path
from .photo_views import PhotoView
from .photoAlbum_views import PhotoAlbunView

urlpatterns = [
    path('photo/add/', PhotoView.as_view(), name='add_photos'),
    path('photo/delete/', PhotoView.as_view(), name='delete_photos'),
    path('photo/revert/', PhotoView.as_view(), name='revert_photos'),
    path('photo/getPhotoListByAlbumId/', PhotoView.as_view(), name='get_photos_by_album_id'),
    path('photo/getAllPhotosByAlbumId/<int:id>/', PhotoView.as_view(), name='get_all_photos_by_album_id'),
    path('photoAlbum/add/', PhotoAlbunView.as_view(), name='add_album'),
    path('photoAlbum/delete/<int:id>/', PhotoAlbunView.as_view(), name='delete_album'),
    path('photoAlbum/update/', PhotoAlbunView.as_view(), name='update_album'),
    path('photoAlbum/', PhotoAlbunView.as_view(), name='get_album_list'),
    path('photoAlbum/getAllAlbumList/', PhotoAlbunView.as_view(), name='get_all_album_list'),
]
