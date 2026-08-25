from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *


@api_view(["GET"])
def subject_list(request):
    limit = request.query_params.get("limit" , 10)

    try:
        limit = int(limit)
    except ValueError:
        return Response({
            "detail": "le parametre doit etre un entier"
        })

    subjects = Subject.objects.order_by("name")[:limit]
    serializer = SubjectSerializer(subjects , many = True)

    return Response(serializer.data)


@api_view(["GET"])
def institution_list(request):
    institutions = Institution.objects.all().order_by("name")

    serializer = InstitutionSerializer(institutions , many = True)

    return Response(
        serializer.data , status=status.HTTP_200_OK
    )

@api_view(["GET"])
def department_list(request):
    departments = Department.objects.select_related("institution")

    serializer = DepartmentSerializer(departments , many = True)
    return Response(
        serializer.data , status=status.HTTP_200_OK
    )

@api_view(["GET"])
def level_list(request):
    levels = Level.objects.all()

    serializer = LevelSerializer(levels, many = True)
    return Response(
        serializer.data , status=status.HTTP_200_OK
    )


@api_view(["GET"])
def exam_list(request):
    exams = ExamType.objects.all()

    serializer = ExamTypeSerializer(exams, many = True)
    return Response(
        serializer.data , status=status.HTTP_200_OK
    )

