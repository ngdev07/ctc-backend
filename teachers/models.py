from django.db import models
from django.conf import settings

from core.models import TimeStampedModel
from academics.models import Institution , Department ,Subject , ExamType

class TeacherProfile(TimeStampedModel):

    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE , related_name="teacher_profile")

    institution = models.ForeignKey(Institution , on_delete=models.PROTECT , related_name="teachers")

    departement = models.ForeignKey(Department , on_delete=models.PROTECT , related_name="teachers")

    bio = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    average_rating = models.PositiveIntegerField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)

    rating  = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class TeacherSubject(TimeStampedModel):
    teacher = models.ForeignKey(TeacherProfile , on_delete=models.CASCADE , related_name="subjects")

    subject = models.ForeignKey(Subject , on_delete=models.CASCADE)

    exam_type = models.ForeignKey(ExamType , on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10 , decimal_places=2)

    is_available = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False)
    class Meta:
        unique_together = (
            "teacher", "subject" , "exam_type"
        )

    def __str__(self):
        return f"{self.teacher.user.username} - {self.subject.name}"