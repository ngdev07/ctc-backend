from django.urls import path
from .views import *

urlpatterns = [
    path("institutions/",institution_list),
    path("departments/" , department_list),
    path("levels/",level_list),
    path("subjects/",subject_list),
    path("exam/",exam_list),

]
