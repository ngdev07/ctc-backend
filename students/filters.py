import django_filters
from django.db.models import Q

from .models import StudentProfile


class StudentFilter(django_filters.FilterSet):
    """
    Filtres disponibles pour rechercher les étudiants.
    """

    # Recherche par prénom, nom ou username.
    search = django_filters.CharFilter(
        method="filter_search"
    )

    # Filtre par établissement.
    # Exemple : ?institution=2
    institution = django_filters.NumberFilter(
        field_name="institution_id"
    )

    # Filtre par département.
    # Exemple : ?department=3
    department = django_filters.NumberFilter(
        field_name="departement_id"
    )

    # Filtre par niveau.
    # Exemple : ?level=1
    level = django_filters.NumberFilter(
        field_name="level_id"
    )

    # Permet de rechercher les comptes actifs ou suspendus.
    # Exemple : ?is_active=true
    is_active = django_filters.BooleanFilter(
        field_name="user__is_active"
    )

    class Meta:
        model = StudentProfile

        fields = (
            "institution",
            "department",
            "level",
            "is_active",
        )

    def filter_search(self, queryset, name, value):
        """
        Recherche l'étudiant par :

        - prénom
        - nom
        - username
        """

        return queryset.filter(
            Q(user__first_name__icontains=value)
            | Q(user__last_name__icontains=value)
            | Q(user__username__icontains=value)
        )