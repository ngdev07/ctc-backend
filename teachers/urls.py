from django.urls import path

from .views import create_teacher, admin_teacher_list , admin_teacher_detail, suspend_teacher, activate_teacher, teacher_list, teacher_detail,teacher_profile, teacher_subjects,teacher_subject_detail

urlpatterns = [

    # ===========================
    # Administration
    # ===========================

    path("admin/teachers/",admin_teacher_list,name="admin_teacher_list"),
    path(
        "admin/teachers/<int:pk>/",
        admin_teacher_detail,
        name="admin_teacher_detail",
    ),

    path(
        "admin/teachers/<int:pk>/suspend/",
        suspend_teacher,
        name="suspend_teacher",
    ),

    path(
        "admin/teachers/<int:pk>/activate/",
        activate_teacher,
        name="activate_teacher",
    ),

    # ===========================
    # Public
    # ===========================

    path(
        "teachers/",
        teacher_list,
        name="teacher_list",
    ),

    path(
        "teachers/<int:pk>/",
        teacher_detail,
        name="teacher_detail",
    ),

    # ===========================
    # Profil professeur
    # ===========================

    path(
        "teacher/profile/",
        teacher_profile,
        name="teacher_profile",
    ),

    # ===========================
    # Matières du professeur
    # ===========================

    path(
        "teacher/subjects/",
        teacher_subjects,
        name="teacher_subjects",
    ),

    path(
        "teacher/subjects/<int:pk>/",
        teacher_subject_detail,
        name="teacher_subject_detail",
    ),



    # admin

    path("create/teachers/",create_teacher , name="admin-create-teacher")
]


