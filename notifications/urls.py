from django.urls import path

from .views import (
    notification_list,
    notification_read,
    notification_read_all,
)


urlpatterns = [
    path(
        "",
        notification_list,
        name="notification-list",
    ),

    path(
        "read/<int:pk>/",
        notification_read,
        name="notification-read",
    ),

    path(
        "read-all/",
        notification_read_all,
        name="notification-read-all",
    ),
]

