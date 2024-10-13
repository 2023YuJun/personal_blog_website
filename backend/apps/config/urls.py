from django.urls import path
from .views import ConfigView

urlpatterns = [
    path('config/', ConfigView.as_view(), name='get_config'),
    path('config/update/', ConfigView.as_view(), name='update_config'),
    path('upload/img/', ConfigView.as_view(), name='upload_img'),
    path('config/addView/', ConfigView.as_view(), name='add_view'),
    path('statistic/', ConfigView.as_view(), name='home_get_statistic'),
]
