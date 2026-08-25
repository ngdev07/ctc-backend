from django.shortcuts import get_object_or_404

from .models import StudentProfile


def get_student_by_id(student_id):
    """
    Récupère un étudiant à partir de son identifiant.

    On utilise cette fonction dans les vues afin d'éviter
    de répéter le même get_object_or_404() partout.
    """

    return get_object_or_404(
        StudentProfile.objects.select_related(
            "user",
            "institution",
            "departement",
            "level",
        ),
        pk=student_id,
    )


def get_student_by_user(user):
    """
    Récupère le profil étudiant associé à l'utilisateur connecté.

    Exemple :
        student = get_student_by_user(request.user)
    """

    return get_object_or_404(
        StudentProfile.objects.select_related(
            "user",
            "institution",
            "departement",
            "level",
        ),
        user=user,
    )


def get_active_students():
    """
    Retourne uniquement les étudiants dont le compte
    utilisateur est actif.

    Cette fonction sera principalement utilisée
    pour les listes visibles sur la plateforme.
    """

    return StudentProfile.objects.select_related(
        "user",
        "institution",
        "departement",
        "level",
    ).filter(
        user__is_active=True
    )


def suspend_student(student):
    """
    Désactive le compte utilisateur de l'étudiant.

    Le profil StudentProfile n'est pas supprimé.
    L'étudiant ne pourra simplement plus utiliser
    son compte tant qu'il est suspendu.
    """

    student.user.is_active = False

    student.user.save(
        update_fields=["is_active"]
    )

    return student


def activate_student(student):
    """
    Réactive le compte utilisateur de l'étudiant.
    """

    student.user.is_active = True

    student.user.save(
        update_fields=["is_active"]
    )

    return student


def delete_student(student):
    """
    Supprime définitivement l'étudiant.

    Le User est supprimé et, grâce au
    OneToOneField avec on_delete=models.CASCADE,
    le StudentProfile associé sera également supprimé.
    """

    student.user.delete()