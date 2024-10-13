from django.urls import path
from .views import UserView
urlpatterns = [
    path('user/register/', UserView.as_view(), name='register'),
    path('user/login/', UserView.as_view(), name='login'),
    path('user/updateOwnUserInfo/', UserView.as_view(), name='update_own_user_info'),
    path('user/updatePassword/', UserView.as_view(), name='update_password'),
    path('user/updateRole/<int:id>/<str:role>/', UserView.as_view(), name='update_role'),
    path('user/adminUpdateUserInfo/', UserView.as_view(), name='admin_update_user_info'),
    path('user/getUserList/', UserView.as_view(), name='get_user_list'),
    path('user/getUserInfoById/<int:id>/', UserView.as_view(), name='get_user_info_by_id'),
]
