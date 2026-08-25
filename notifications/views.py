from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def notification_list(request):

    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by("-created_at")

    serializer = NotificationSerializer(
        notifications,
        many=True
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )
    
@api_view(["PATCH"])
# @permission_classes([IsAuthenticated])
def notification_read(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        recipient=request.user,
    )

    notification.is_read = True

    notification.save(
        update_fields=[
            "is_read",
            "updated_at",
        ]
    )

    return Response(
        {
            "detail": "Notification marquée comme lue."
        },
        status=status.HTTP_200_OK
    )
    
    
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def notification_read_all(request):

    Notification.objects.filter(
        recipient=request.user,
        is_read=False,
    ).update(
        is_read=True
    )

    return Response(
        {
            "detail": "Toutes les notifications sont marquées comme lues."
        },
        status=status.HTTP_200_OK
    )
    
    
    