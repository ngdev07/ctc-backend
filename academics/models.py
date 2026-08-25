from django.db import models
from core.models import TimeStampedModel

class Institution(models.Model):
    name = models.CharField(max_length=150 , unique=True)
    abbreviation = models.CharField(max_length=20 , unique=True)

    is_active = models.BooleanField(default=True)

    class Meta :
        ordering = ["name"]

    def __str__(self):
        return self.abbreviation 



class Department(TimeStampedModel):

    institution = models.ForeignKey(Institution , on_delete=models.CASCADE , related_name="departments")
    name = models.CharField(max_length=150)
    abbreviation = models.CharField(max_length=20)

    is_active = models.BooleanField(default=True)


    class Meta:
        ordering = ["name"]
        constraints = [ models.UniqueConstraint (fields= ["institution", "name"], name = "unique_department_per_institution") ]


    def __str__(self):
        return f"{self.name}({self.abbreviation})"


class Level(models.Model):
    name = models.CharField(max_length=50 , unique= True)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class Subject(models.Model):
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    level = models.ForeignKey(Level , on_delete=models.PROTECT ,null=True , blank=True, related_name="subjects")

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]


    def __str__(self):
        return f"{self.name}({self.code})   {self.level.name}"


class ExamType(models.Model):
    name =models.CharField(max_length=30 ,unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name