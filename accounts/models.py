from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    class Role(models.TextChoices):
        admin = "admin" , "administrateur"
        teacher = 'teacher' , 'professeur',
        student = 'student' , 'etudiant'


    email = models.EmailField(max_length=190, unique=True);
    username = models.CharField(max_length=150 )


    role = models.CharField(max_length=20 , choices=Role.choices , default=Role.student)
    phone = PhoneNumberField(
        region = "CM",
        blank=True,
        null=True
    )

    profile = models.ImageField(upload_to="profiles/" , default="profiles/default.png" , blank=True)
    is_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    must_change_password = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    Updated_at  = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}  ({self.role})"