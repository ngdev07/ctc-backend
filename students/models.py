from django.db import models
from django.conf import settings
from core.models import TimeStampedModel
from academics.models import Institution , Department , Level


class StudentProfile(TimeStampedModel):
     user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE , related_name="student_profile")
    
     institution = models.ForeignKey(Institution , on_delete=models.PROTECT , related_name="students")
    
     departement = models.ForeignKey(Department , on_delete=models.PROTECT , related_name="students")
     level = models.ForeignKey(Level , on_delete=models.PROTECT ,related_name="students")

     matricule = models.CharField(max_length=30 , blank=True , null = True)

     def __str__(self):
            return self.user.get_full_name() or self.user.username    