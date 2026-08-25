from rest_framework import serializers

from .models import StudentProfile


class StudentListSerializer(serializers.ModelSerializer):
    """
    Serializer léger utilisé pour les listes d'étudiants.

    Il sera utilisé notamment :
    - dans l'administration ;
    - dans la recherche ;
    - éventuellement sur la page d'accueil.
    """

    # Nom complet provenant du modèle User.
    full_name = serializers.SerializerMethodField()

    # Email provenant du modèle User.
    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    # Nom de l'établissement.
    institution_name = serializers.CharField(
        source="institution.name",
        read_only=True
    )

    # Nom du département.
    department_name = serializers.CharField(
        source="departement.name",
        read_only=True
    )

    # Nom du niveau.
    level_name = serializers.CharField(
        source="level.name",
        read_only=True
    )

    # Permet de savoir si le compte est actif ou suspendu.
    is_active = serializers.BooleanField(
        source="user.is_active",
        read_only=True
    )

    class Meta:
        model = StudentProfile

        fields = (
            "id",
            "full_name",
            "email",
            "institution",
            "institution_name",
            "departement",
            "department_name",
            "level",
            "level_name",
            "matricule",
            "is_active",
        )

    def get_full_name(self, obj):
        """
        Retourne le nom complet de l'étudiant.

        Si aucun nom n'est enregistré,
        on utilise le username.
        """

        full_name = obj.user.get_full_name()

        return (
            full_name
            if full_name
            else obj.user.username
        )


class StudentDetailSerializer(serializers.ModelSerializer):
    """
    Serializer utilisé pour afficher les détails
    complets d'un étudiant.
    """

    # Nom complet de l'étudiant.
    full_name = serializers.SerializerMethodField()

    # Informations provenant du User.
    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    phone_number = serializers.CharField(
        source="user.phone_number",
        read_only=True
    )

    # Informations académiques lisibles.
    institution_name = serializers.CharField(
        source="institution.name",
        read_only=True
    )

    department_name = serializers.CharField(
        source="departement.name",
        read_only=True
    )

    level_name = serializers.CharField(
        source="level.name",
        read_only=True
    )

    # État du compte.
    is_active = serializers.BooleanField(
        source="user.is_active",
        read_only=True
    )

    class Meta:
        model = StudentProfile

        fields = (
            "id",
            "full_name",
            "email",
            "phone_number",
            "institution",
            "institution_name",
            "departement",
            "department_name",
            "level",
            "level_name",
            "matricule",
            "is_active",
            "created_at",
            "updated_at",
        )

        # Ces champs sont gérés automatiquement
        # par Django ou proviennent du User.
        read_only_fields = (
            "created_at",
            "updated_at",
            "is_active",
        )

    def get_full_name(self, obj):
        """
        Retourne le nom complet de l'étudiant.
        """

        full_name = obj.user.get_full_name()

        return (
            full_name
            if full_name
            else obj.user.username
        )


class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer utilisé lorsqu'un étudiant modifie
    son profil académique.
    """

    class Meta:
        model = StudentProfile

        fields = (
            "institution",
            "departement",
            "level",
            "matricule",
        )