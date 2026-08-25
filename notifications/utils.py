from .models import Notification


def create_notification(
    recipient,
    notification_type,
    title,
    message,
):
    """
    Crée une notification pour un utilisateur.
    """

    return Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
    )
    
    