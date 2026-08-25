import django_filters
from django.db.models import Q

from .models import TeacherProfile


class TeacherFilter(django_filters.FilterSet):
    """
    Filtres disponibles pour la recherche des professeurs.
    """

    # Recherche par prénom, nom ou nom d'utilisateur.
    search = django_filters.CharFilter(
        method="filter_search"
    )

    # Filtre par établissement.
    institution = django_filters.NumberFilter(
        field_name="institution_id"
    )

    # Filtre par département.
    department = django_filters.NumberFilter(
        field_name="departement_id"
    )

    # Filtre par état du compte.
    is_active = django_filters.BooleanFilter(
        field_name="user__is_active"
    )

    # Nombre minimum d'années d'expérience.
    min_experience = django_filters.NumberFilter(
        field_name="experience_years",
        lookup_expr="gte"
    )

    # Nombre minimum d'avis.
    min_reviews = django_filters.NumberFilter(
        field_name="total_reviews",
        lookup_expr="gte"
    )

    # Note moyenne minimale.
    min_average_rating = django_filters.NumberFilter(
        field_name="average_rating",
        lookup_expr="gte"
    )

    # Tri des résultats.
    ordering = django_filters.OrderingFilter(

        fields=(

            ("created_at", "created_at"),

            ("experience_years", "experience_years"),

            ("average_rating", "average_rating"),

            ("total_reviews", "total_reviews"),

        )
    )

    class Meta:
        model = TeacherProfile

        fields = (
            "institution",
            "department",
            "is_active",
        )

    def filter_search(self, queryset, name, value):
        """
        Recherche un professeur à partir :

        - du prénom
        - du nom
        - du nom d'utilisateur
        """

        return queryset.filter(

            Q(user__first_name__icontains=value)

            | Q(user__last_name__icontains=value)

            | Q(user__username__icontains=value)

        )