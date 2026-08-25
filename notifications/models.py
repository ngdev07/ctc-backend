from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class NotificationType(models.TextChoices):
    BOOKING_REQUEST = "BOOKING_REQUEST", "Nouvelle demande"
    BOOKING_ACCEPTED = "BOOKING_ACCEPTED", "Demande acceptée"
    BOOKING_REJECTED = "BOOKING_REJECTED", "Demande refusée"
    BOOKING_CANCELLED = "BOOKING_CANCELLED", "Demande annulée"


class Notification(TimeStampedModel):
    """
    Notification destinée à un utilisateur.
    """

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices,
    )

    title = models.CharField(
        max_length=150
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.recipient} - {self.title}"