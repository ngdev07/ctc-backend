from django.urls import path

from .views import (
    # =========================
    # Administration
    # =========================
    admin_student_list,
    admin_student_detail,
    suspend_student_view,
    activate_student_view,
    delete_student_view,

    # =========================
    # Public
    # =========================
    student_list,
    student_detail,

    # =========================
    # Étudiant connecté
    # =========================
    student_profile,
)


urlpatterns = [

    # ==========================================
    # ADMINISTRATION DES ÉTUDIANTS
    # ==========================================

    # Liste des étudiants
    # GET /api/admin/students/
    path(
        "admin/students/",
        admin_student_list,
        name="admin_student_list",
    ),

    # Détail d'un étudiant
    # GET /api/admin/students/<id>/
    path(
        "admin/students/<int:pk>/",
        admin_student_detail,
        name="admin_student_detail",
    ),

    # Suspendre un étudiant
    # PATCH /api/admin/students/<id>/suspend/
    path(
        "admin/students/suspend/<int:pk>",
        suspend_student_view,
        name="suspend_student",
    ),

    # Activer un étudiant
    # PATCH /api/admin/students/<id>/activate/
    path(
        "admin/students/activate/<int:pk>",
        activate_student_view,
        name="activate_student",
    ),

    # Supprimer un étudiant
    # DELETE /api/admin/students/<id>/
    path(
        "admin/students/delete/<int:pk>",
        delete_student_view,
        name="delete_student",
    ),


    # ==========================================
    # ÉTUDIANTS VISIBLES SUR LA PLATEFORME
    # ==========================================

    # Liste des étudiants actifs
    # GET /api/students/
    path(
        "students/",
        student_list,
        name="student_list",
    ),

    # Détail d'un étudiant actif
    # GET /api/students/<id>/
    path(
        "students/<int:pk>/",
        student_detail,
        name="student_detail",
    ),


    # ==========================================
    # PROFIL DE L'ÉTUDIANT CONNECTÉ
    # ==========================================

    # Consulter ou modifier son profil
    # GET   /api/student/profile/
    # PATCH /api/student/profile/
    path(
        "student/profile/",
        student_profile,
        name="student_profile",
    ),
]