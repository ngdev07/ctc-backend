from rest_framework import serializers
from .models import Subject, Institution ,Department , Level  ,ExamType


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = "__all__"

class DepartmentSerializer(serializers.ModelSerializer):
    institution  = serializers.StringRelatedField()

    class Meta:
        model = Department
        fields = "__all__"


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = "__all__"

class SubjectSerializer(serializers.ModelSerializer):
    level  = serializers.StringRelatedField()

    class Meta:
        model = Subject
        fields = "__all__"


class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamType
        fields = "__all__"

