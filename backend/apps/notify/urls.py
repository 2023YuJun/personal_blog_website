from django.urls import path
from .views import NotifyView

urlpatterns = [
    path('notify/update/<int:id>/', NotifyView.as_view(), name='update_notify'),
    path('notify/delete/<int:id>/', NotifyView.as_view(), name='delete_notifys'),
    path('notify/getNotifyList/', NotifyView.as_view(), name='get_notify_list'),
]
