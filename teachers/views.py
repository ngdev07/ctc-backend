from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.response import Response
from core.pagination import AdminTeacherPagination
from .models import TeacherProfile , TeacherSubject
from .serializers import TeacherAdminDetailSerializer ,TeacherAdminListSerializer

from django.db import transaction

User = get_user_model()
@api_view(["GET"])
# @permission_classes([IsAdminUser , IsAuthenticated])
def admin_teacher_list(request):
    teachers = TeacherProfile.objects.select_related("user", "department")


    search = request.query_params.get('search')

    if search:
        teachers = teachers.filter(
            Q(user__first_name__icontains = search) |
            Q(user__last_name__icontains=search) |
            Q(user__username__icontains=search)
        )


    department = request.query_params.get("department")

    if department:
        teachers = teachers.filter(department_id = department)


    is_active = request.query_params.get("is_active")

    if is_active is not None:
        if is_active.lower() == "true":
            teachers = teachers.filter(user__is_active = True)

        elif is_active.lower() == "false":
            teachers = teachers.filter(user__is_active = False)


    ordering = request.query_params.get("ordering", "-created_at")

    allowed_ordering = {
        "first_name": "user__first_name",
        "-first_name": "-user_first_name",
        "last_name": "user__last_name",
        "-last_name": "-user__last_name",
        "created_at" : "created_at",
        "-created_at" : "-created_at"
    }

    ordering = allowed_ordering.get(ordering , "-created_at")

    teachers = teachers.order_by(ordering)

    paginator = AdminTeacherPagination()

    page  = paginator.paginate_queryset(teachers , request)

    serializer = TeacherAdminListSerializer(page , many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def admin_teacher_detail(request,pk):

    teacher = get_object_or_404(TeacherProfile.objects.select_related("user", "department"), pk = pk)

    serializer = TeacherAdminDetailSerializer(teacher)

    return Response(serializer.data , status=status.HTTP_200_OK)



@api_view(["PATCH"])
# @permission_classes([IsAuthenticated ,IsAdmin])
def admin_teacher_suspend(request, pk):

    teacher = get_object_or_404(TeacherProfile,pk=pk)
    teacher.user.is_active = False
    teacher.use.save (
        update_fields = ["is_active"]
    )

    return Response(
        {
            "success": True,
            "message": "",

        },
        status= status.HTTP_200_OK
    )


@api_view(["PATCH"])
# @permission_classes([IsAuthenticated ,IsAdmin])
def admin_teacher_activate(request, pk):

    teacher = get_object_or_404(TeacherProfile,pk=pk)
    teacher.user.is_active = True
    teacher.use.save (
        update_fields = ["is_active"]
    )

    return Response(
        {
            "success": True,
            "message": "",

        },
        status= status.HTTP_200_OK
    )

@api_view(["DELETE"])
# @permission_classes([IsAuthenticated ,IsAdmin])
def admin_teacher_delete(request, pk):

    teacher = get_object_or_404(TeacherProfile,pk=pk)
    teacher.user.is_active = False

    user = teacher.user

    teacher.delete()
    user.delete()

    return Response(
        {
            "success": True,
            "message": "",

        },
        status= status.HTTP_200_OK
    )


from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)

# from accounts.permissions import IsAdmin

from core.utils import (
    success_response,
    error_response,
)

from core.constants import (
    DELETED,
)

from .filter import TeacherFilter

from .models import TeacherProfile

from .serializers import (
    TeacherListSerializer,
    TeacherDetailSerializer,
)

from core.pagination import DefaultPagination

@api_view(["GET"])
# @permission_classes([IsAuthenticated, IsAdmin])
def admin_teacher_list(request):
    """
    Retourne la liste des professeurs.

    Filtres disponibles :

    - search
    - institution
    - department
    - is_active
    - min_reviews
    - min_average_rating
    - min_experience
    """

    teachers = TeacherProfile.objects.select_related(
        "user",
        "institution",
        "departement",
    )

    teacher_filter = TeacherFilter(
        request.GET,
        queryset=teachers
    )

    teachers = teacher_filter.qs

    paginator = DefaultPagination()

    page = paginator.paginate_queryset(
        teachers,
        request
    )

    serializer = TeacherListSerializer(
        page,
        many=True
    )

    return paginator.get_paginated_response(
        serializer.data
    )
    
    
@api_view(["GET", "DELETE"])
# @permission_classes([IsAuthenticated, IsAdmin])
def admin_teacher_detail(request, pk):
    """
    Retourne les détails d'un professeur
    ou le supprime.
    """

    teacher = get_object_or_404(
        TeacherProfile.objects.select_related(
            "user",
            "institution",
            "departement",
        ),
        pk=pk,
    )

    if request.method == "GET":

        serializer = TeacherDetailSerializer(
            teacher
        )

        return success_response(
            data=serializer.data
        )

    teacher.user.delete()

    return success_response(
        message=DELETED
    )
    
@api_view(["PATCH"])
# @permission_classes([IsAuthenticated, IsAdmin])
def suspend_teacher(request, pk):
    """
    Suspend un professeur.
    """

    teacher = get_object_or_404(
        TeacherProfile,
        pk=pk
    )

    teacher.user.is_active = False

    teacher.user.save(
        update_fields=[
            "is_active",
        ]
    )

    return success_response(
        message="Professeur suspendu avec succès."
    )
    
@api_view(["PATCH"])
# @permission_classes([IsAuthenticated, IsAdmin])
def activate_teacher(request, pk):
    """
    Réactive un professeur.
    """

    teacher = get_object_or_404(
        TeacherProfile,
        pk=pk
    )

    teacher.user.is_active = True

    teacher.user.save(
        update_fields=[
            "is_active",
        ]
    )

    return success_response(
        message="Professeur activé avec succès."
    )
    
    
@api_view(["GET"])
def teacher_list(request):
    """
    Retourne la liste des professeurs actifs.

    Filtres disponibles :

    - search
    - institution
    - department
    - min_reviews
    - min_average_rating
    - min_experience
    """

    # Seuls les professeurs actifs sont visibles
    teachers = TeacherProfile.objects.select_related(
        "user",
        "institution",
        "departement",
    ).filter(
        user__is_active=True
    )

    # Application des filtres
    teacher_filter = TeacherFilter(
        request.GET,
        queryset=teachers
    )

    teachers = teacher_filter.qs

    # Pagination
    paginator = DefaultPagination()

    page = paginator.paginate_queryset(
        teachers,
        request
    )

    serializer = TeacherListSerializer(
        page,
        many=True
    )

    return paginator.get_paginated_response(
        serializer.data
    )


@api_view(["GET"])
def teacher_detail(request, pk):
    """
    Retourne les informations détaillées
    d'un professeur.
    """

    teacher = get_object_or_404(
        TeacherProfile.objects.select_related(
            "user",
            "institution",
            "departement",
        ).prefetch_related(
            "subjects",
        ),
        pk=pk,
        user__is_active=True,
    )

    serializer = TeacherDetailSerializer(
        teacher
    )

    return success_response(
        data=serializer.data
    )
    
    from .models import TeacherSubject

from .serializers import (
    TeacherSubjectSerializer,
)

from accounts.permissions import IsTeacher


@api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated, IsTeacher])
def teacher_subjects(request):
    """
    Retourne les matières du professeur connecté
    ou permet d'en créer une nouvelle.
    """

    teacher = request.user.teacher_profile

    if request.method == "GET":

        subjects = TeacherSubject.objects.select_related(
            "subject",
            "exam_type",
        ).filter(
            teacher=teacher
        ).order_by(
            "subject__name"
        )

        serializer = TeacherSubjectSerializer(
            subjects,
            many=True
        )

        return success_response(
            data=serializer.data
        )

    serializer = TeacherSubjectSerializer(
        data=request.data
    )

    if not serializer.is_valid():

        return error_response(
            message="Données invalides.",
            errors=serializer.errors
        )

    subject = TeacherSubject.objects.create(
        teacher=teacher,
        **serializer.validated_data
    )

    return success_response(
        data=TeacherSubjectSerializer(subject).data,
        message="Matière ajoutée avec succès.",
        status_code=201
    )
    
    
@api_view(["GET", "PATCH", "DELETE"])
# @permission_classes([IsAuthenticated, IsTeacher])
def teacher_subject_detail(request, pk):
    """
    Gère une matière du professeur connecté.
    """

    teacher = request.user.teacher_profile

    teacher_subject = get_object_or_404(
        TeacherSubject.objects.select_related(
            "subject",
            "exam_type",
        ),
        pk=pk,
        teacher=teacher,
    )

    if request.method == "GET":

        serializer = TeacherSubjectSerializer(
            teacher_subject
        )

        return success_response(
            data=serializer.data
        )

    if request.method == "PATCH":

        serializer = TeacherSubjectSerializer(
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():

            return error_response(
                message="Données invalides.",
                errors=serializer.errors
            )

        for field, value in serializer.validated_data.items():
            setattr(
                teacher_subject,
                field,
                value
            )

        teacher_subject.save()

        return success_response(
            data=TeacherSubjectSerializer(
                teacher_subject
            ).data,
            message="Matière modifiée avec succès."
        )

    teacher_subject.delete()

    return success_response(
        message="Matière supprimée avec succès."
    )
    
    
class TeacherProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer utilisé par le professeur
    pour modifier son profil.
    """

    class Meta:
        model = TeacherProfile

        fields = (
            "institution",
            "departement",
            "bio",
            "experience_years",
        )
        
        
        
@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated, IsTeacher])
def teacher_profile(request):
    """
    Consulter ou modifier son profil professeur.
    """

    teacher = get_object_or_404(
        TeacherProfile.objects.select_related(
            "user",
            "institution",
            "departement",
        ).prefetch_related(
            "subjects"
        ),
        user=request.user
    )

    if request.method == "GET":

        serializer = TeacherDetailSerializer(
            teacher
        )

        return success_response(
            data=serializer.data
        )

    serializer = TeacherProfileUpdateSerializer(
        teacher,
        data=request.data,
        partial=True
    )

    if not serializer.is_valid():

        return error_response(
            message="Données invalides.",
            errors=serializer.errors
        )

    serializer.save()

    return success_response(
        data=TeacherDetailSerializer(teacher).data,
        message="Profil mis à jour avec succès."
    )
    
    

@api_view(["POST"])
# @permission_classes([IsAuthenticated , IsAdminUser])
def create_teacher(request):

    email = request.data.get("email")
    password = request.data.get("password")
    username = request.data.get("username")
    
    
    if not email or not username or not password:
            return Response({
                "success": False,
                "message":(
                    "Informations requises"
                )
            } , status= status.HTTP_400_BAD_REQUEST)
    
    
    if User.objects.filter(email__iexact = email).exists():
            return({
                "success": False,
                "message": "Cette adresse email est deja utilise",
            } ,  status.HTTP_409_CONFLICT)
        
    if User.objects.filter(username__iexact = username).exists():
                return({
                    "success": False,
                    "message": "Ce nom d'utilisateur est deja utilise",
                } ,  status.HTTP_409_CONFLICT)
    
    
    with transaction.atomic():
    
            user = User.objects.create_user(
                email=email,
                username= username,
                password=password,
                role =  'teacher',
            )
    
            teacher_profil = TeacherProfile.objects.create(user = user)
    
            return Response({
                "success": True,
                "message": "Compte etudiant crée avec succes",
                "data" : TeacherDetailSerializer(user).data
    
            } ,  status.HTTP_201_CREATED)