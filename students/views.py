from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated

# from accounts.permissions import IsAdmin, IsStudent

from core.utils import (
    success_response,
    error_response,
)

from core.pagination import DefaultPagination

from .models import StudentProfile

from .filters import StudentFilter

from .serializers import (
    StudentListSerializer,
    StudentDetailSerializer,
    StudentProfileUpdateSerializer,
)

from .utils import (
    get_student_by_id,
    get_student_by_user,
    get_active_students,
    suspend_student,
    activate_student,
    delete_student,
)


@api_view(["GET"])
# @permission_classes([IsAuthenticated, IsAdmin])
def admin_student_list(request):
    """
    Retourne la liste des étudiants pour l'administration.

    Les résultats peuvent être filtrés avec :

    - search
    - institution
    - department
    - level
    - is_active

    La liste est paginée.
    """

    # Récupère les étudiants avec leurs relations
    # afin d'éviter des requêtes SQL supplémentaires.
    students = StudentProfile.objects.select_related(
        "user",
        "institution",
        "departement",
        "level",
    )

    # Application des filtres reçus dans request.GET.
    student_filter = StudentFilter(
        request.GET,
        queryset=students,
    )

    # Queryset final après filtrage.
    students = student_filter.qs

    # Création du paginator.
    paginator = DefaultPagination()

    # Récupération de la page demandée.
    page = paginator.paginate_queryset(
        students,
        request,
    )

    # Transformation des objets Django en JSON.
    serializer = StudentListSerializer(
        page,
        many=True,
    )

    # Retourne les résultats avec les informations
    # de pagination.
    return paginator.get_paginated_response(
        serializer.data
    )
    
    
@api_view(["GET"])
# @permission_classes([IsAuthenticated, IsAdmin])
def admin_student_detail(request, pk):
    """
    Retourne les informations détaillées
    d'un étudiant.
    """

    # Récupère l'étudiant ou retourne automatiquement
    # une erreur 404 s'il n'existe pas.
    student = get_student_by_id(pk)

    # Transforme le StudentProfile en JSON.
    serializer = StudentDetailSerializer(
        student
    )

    return success_response(
        data=serializer.data
    )
    
    
    
@api_view(["PATCH"])
# @permission_classes([IsAuthenticated, IsAdmin])
def suspend_student_view(request, pk):
    """
    Suspend le compte d'un étudiant.

    Le StudentProfile n'est pas supprimé.
    Seul le compte User est désactivé.
    """

    # Récupère l'étudiant.
    student = get_student_by_id(pk)

    # Désactive son compte.
    suspend_student(student)

    return success_response(
        message="Étudiant suspendu avec succès."
    )
    

@api_view(["PATCH"])
# @permission_classes([IsAuthenticated, IsAdmin])
def activate_student_view(request, pk):
    """
    Réactive le compte d'un étudiant.
    """

    # Récupère l'étudiant.
    student = get_student_by_id(pk)

    # Réactive son compte.
    activate_student(student)

    return success_response(
        message="Étudiant activé avec succès."
    )
    
@api_view(["DELETE"])
# @permission_classes([IsAuthenticated, IsAdmin])
def delete_student_view(request, pk):
    """
    Supprime définitivement un étudiant.
    """

    # Récupère l'étudiant.
    student = get_student_by_id(pk)

    # Supprime son compte.
    delete_student(student)

    return success_response(
        message="Étudiant supprimé avec succès."
    )
    
    
@api_view(["GET"])
def student_list(request):
    """
    Retourne la liste des étudiants actifs.

    Cette liste peut être filtrée par :

    - nom
    - établissement
    - département
    - niveau
    """

    # On ne montre jamais les comptes suspendus.
    students = get_active_students()

    # Application des filtres.
    student_filter = StudentFilter(
        request.GET,
        queryset=students,
    )

    students = student_filter.qs

    # Pagination.
    paginator = DefaultPagination()

    page = paginator.paginate_queryset(
        students,
        request,
    )

    serializer = StudentListSerializer(
        page,
        many=True,
    )

    return paginator.get_paginated_response(
        serializer.data
    )
    
    
@api_view(["GET"])
def student_detail(request, pk):
    """
    Retourne les informations publiques
    d'un étudiant actif.
    """

    student = get_object_or_404(
        StudentProfile.objects.select_related(
            "user",
            "institution",
            "departement",
            "level",
        ),
        pk=pk,
        user__is_active=True,
    )

    serializer = StudentDetailSerializer(
        student
    )

    return success_response(
        data=serializer.data
    )
    
    
@api_view(["GET", "PATCH"])
# @permission_classes([IsAuthenticated, IsStudent])
def student_profile(request):
    """
    Permet à l'étudiant connecté :

    - de consulter son profil ;
    - de modifier ses informations académiques.
    """

    # Récupère le profil associé au compte connecté.
    student = get_student_by_user(
        request.user
    )

    # =========================
    # GET
    # =========================

    if request.method == "GET":

        serializer = StudentDetailSerializer(
            student
        )

        return success_response(
            data=serializer.data
        )

    # =========================
    # PATCH
    # =========================

    serializer = StudentProfileUpdateSerializer(
        student,
        data=request.data,
        partial=True,
    )

    # Vérification des données reçues.
    if not serializer.is_valid():

        return error_response(
            message="Données invalides.",
            errors=serializer.errors,
        )

    # Enregistre les modifications.
    serializer.save()

    # Retourne le profil mis à jour.
    return success_response(
        data=StudentDetailSerializer(
            student
        ).data,
        message="Profil mis à jour avec succès.",
    )
    
    
    