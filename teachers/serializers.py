from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import TeacherProfile

class TeacherAdminListSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()
    email = serializers.CharField(source = "user.email" , read_only = True)

    username = serializers.CharField(source = "user.username" , read_only = True)
    is_active = serializers.BooleanField(source = "user.is_active" , read_only = True)
    department_name = serializers.CharField(source = "user.department.name" , read_only = True)

    phone = PhoneNumberField(region="CM")
    class Meta:
        model = TeacherProfile
        fields = (
            "id",
            "full_name",
            "username",
            "email",
            "department",
            "department_name",
            "is_active",
            "created_at",
        )


    def get_full_name(self,obj):
        return obj.user.get_full_name()



class TeacherAdminDetailSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()
    email = serializers.CharField(source = "user.email" , read_only = True)

    username = serializers.CharField(source = "user.username" , read_only = True)
    is_active = serializers.BooleanField(source = "user.is_active" , read_only = True)
    department_name = serializers.CharField(source = "user.department.name" , read_only = True)
    institution_name = serializers.CharField(source = "user.institution.name" , read_only = True)



    class Meta:
        model = TeacherProfile
        fields = (
            "id",
            "full_name",
            "username",
            "email",
            "department",
            "department_name",
            "institution_name"
            "is_active",
            "created_at",
            "image",
            "updated_at",
            "bio",
            'average_rating',
            'experience_years',
            'total_views',
            "phone"
        )


  
    def get_full_name(self,obj):
        return obj.user.get_full_name()


from rest_framework import serializers

from .models import TeacherProfile, TeacherSubject


class TeacherSubjectSerializer(serializers.ModelSerializer):
    """
    Serializer utilisé pour afficher une matière enseignée
    par un professeur.
    """

    # Nom de la matière
    subject_name = serializers.CharField(
        source="subject.name",
        read_only=True
    )

    # Nom du type d'examen
    exam_type_name = serializers.CharField(
        source="exam_type.name",
        read_only=True
    )

    class Meta:
        model = TeacherSubject

        fields = (
            "id",
            "subject",
            "subject_name",
            "exam_type",
            "exam_type_name",
            "price",
            "is_available",
            "is_primary",
            "created_at",
            "updated_at",
        )

        # Ces champs ne peuvent pas être modifiés
        # directement par le client.
        read_only_fields = (
            "created_at",
            "updated_at",
        )


class TeacherListSerializer(serializers.ModelSerializer):
    """
    Serializer utilisé pour la liste des professeurs.

    Exemple :
    - Page d'accueil
    - Résultat de recherche
    """

    # Nom complet du professeur
    full_name = serializers.SerializerMethodField()

    # Informations provenant du modèle User
    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    phone_number = serializers.CharField(
        source="user.phone_number",
        read_only=True
    )

    # Nom de l'établissement
    institution_name = serializers.CharField(
        source="institution.name",
        read_only=True
    )

    # Nom du département
    department_name = serializers.CharField(
        source="departement.name",
        read_only=True
    )

    class Meta:
        model = TeacherProfile

        fields = (
            "id",
            "full_name",
            "email",
            "phone_number",
            "institution",
            "institution_name",
            "departement",
            "department_name",
            "experience_years",
            "average_rating",
            "total_reviews",
        )

    def get_full_name(self, obj):
        """
        Retourne le nom complet.

        Si le prénom et le nom sont vides,
        on retourne le username.
        """

        full_name = obj.user.get_full_name()

        return full_name if full_name else obj.user.username


class TeacherDetailSerializer(serializers.ModelSerializer):
    """
    Serializer utilisé pour afficher
    les détails d'un professeur.
    """

    full_name = serializers.SerializerMethodField()

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    phone_number = serializers.CharField(
        source="user.phone_number",
        read_only=True
    )

    institution_name = serializers.CharField(
        source="institution.name",
        read_only=True
    )

    department_name = serializers.CharField(
        source="departement.name",
        read_only=True
    )

    # Liste des matières enseignées
    subjects = TeacherSubjectSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = TeacherProfile

        fields = (
            "id",
            "full_name",
            "email",
            "phone_number",
            "institution",
            "institution_name",
            "departement",
            "department_name",
            "bio",
            "experience_years",
            "average_rating",
            "total_reviews",
            "rating",
            "subjects",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "created_at",
            "updated_at",
        )

    def get_full_name(self, obj):
        """
        Retourne le nom complet.

        Si aucun prénom/nom n'est renseigné,
        on retourne le username.
        """

        full_name = obj.user.get_full_name()

        return full_name if full_name else obj.user.username