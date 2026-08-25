from django.db import models
from django.conf import  settings
from core.models import TimeStampedModel
from teachers.models import TeacherSubject

User = settings.AUTH_USER_MODEL


class BookingStatus(models.TextChoices):
    pending = "pending" , "en attente"
    accepted = "accepted" , "acceptée"
    rejected = "rejeted" , "refusée"
    cancelled = "cancelled" , "annulée"


class BookingRequest(TimeStampedModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE , related_name="booking_requests")
    teacher_subject = models.ForeignKey(TeacherSubject , on_delete=models.CASCADE , related_name="booking_requests")

    proposed_price = models.DecimalField(max_digits=10 , decimal_places=2)
    message = models.TextField(blank=True)

    status = models.CharField(max_length=20 , choices=BookingStatus.choices , default=BookingStatus.pending)
    rejection_reason = models.TextField(blank=True)

    responded_at =  models.DateTimeField(null=True , blank= True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=["student" , "teacher_subject"], name = "unique_booking_request"
            )
        ]


    def __str__(self):
        return f"{self.student} -> {self.teacher_subject}"