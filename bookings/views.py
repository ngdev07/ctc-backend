from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsStudent, IsTeacher

from teachers.models import TeacherSubject

from .models import BookingRequest, BookingStatus
from .serializers import (
    BookingCreateSerializer,
    BookingListSerializer,
    BookingDetailSerializer,
)

from notifications.utils import create_notification

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsStudent])
def create_booking(request):

    serializer = BookingCreateSerializer(
        data=request.data
    )

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    teacher_subject = get_object_or_404(
        TeacherSubject,
        pk=serializer.validated_data["teacher_subject"].id
    )

    # L'offre doit être active
    if not teacher_subject.is_active:
        return Response(
            {
                "detail": "Cette offre n'est plus disponible."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Une seule disponibilité = un seul étudiant.
    # Si elle est déjà réservée, on refuse la demande.
    if teacher_subject.is_booked:
        return Response(
            {
                "detail": "Cette disponibilité est déjà réservée."
            },
            status=status.HTTP_409_CONFLICT
        )

    # Vérifier que l'étudiant n'a pas déjà
    # une demande active pour cette offre.
    existing_booking = BookingRequest.objects.filter(
        student=request.user,
        teacher_subject=teacher_subject,
        status__in=[
            BookingStatus.PENDING,
            BookingStatus.ACCEPTED,
        ]
    ).exists()

    if existing_booking:
        return Response(
            {
                "detail": "Vous avez déjà une demande pour cette offre."
            },
            status=status.HTTP_409_CONFLICT
        )

    booking = serializer.save(
        student=request.user
    )
    teacher = teacher_subject.teacher.user
    message = f"l'etudiant {request.user.username} vous a envoye une demande pour le cours de {teacher_subject.subject.name}" 
    create_notification(recipient=teacher , notification_type="BOOKING_REQUEST" , title="Nouvelle demande de cours " , 
                        message=message )

    return Response(
        BookingDetailSerializer(booking).data,
        status=status.HTTP_201_CREATED
    )
    
    
@api_view(["GET"])
# @permission_classes([IsAuthenticated, IsStudent])
def my_bookings(request):

    bookings = BookingRequest.objects.filter(
        student=request.user
    ).select_related(
        "teacher_subject",
        "teacher_subject__teacher",
        "teacher_subject__subject",
    )

    serializer = BookingListSerializer(
        bookings,
        many=True
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )
    
    
@api_view(["GET"])
# @permission_classes([IsAuthenticated, IsStudent])
def booking_detail(request, pk):

    booking = get_object_or_404(
        BookingRequest.objects.select_related(
            "teacher_subject",
            "teacher_subject__teacher",
            "teacher_subject__subject",
        ),
        pk=pk,
        student=request.user
    )

    serializer = BookingDetailSerializer(
        booking
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )
    
@api_view(["PATCH"])
# @permission_classes([IsAuthenticated, IsStudent])
def cancel_booking(request, pk):

    booking = get_object_or_404(
        BookingRequest,
        pk=pk,
        student=request.user
    )

    if booking.status != BookingStatus.PENDING:
        return Response(
            {
                "detail": (
                    "Seule une demande en attente "
                    "peut être annulée."
                )
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    booking.status = BookingStatus.CANCELLED
    booking.save(
        update_fields=["status", "updated_at"]
    )

    message = f"votre demande pour le cours de {booking.teacher_subject.subject.name} a ete annule"
    create_notification(recipient=booking.teacher_subject.teacher.user , notification_type="BOOKING_CANCELLED" , title="Demande annule" ,message=message)
    return Response(
        {
            "detail": "Demande annulée avec succès."
        },
        status=status.HTTP_200_OK
    )
    
    
@api_view(["GET"])
# @permission_classes([IsAuthenticated, IsTeacher])
def teacher_bookings(request):

    bookings = BookingRequest.objects.filter(
        teacher_subject__teacher=request.user.teacher_profile
    ).select_related(
        "student",
        "teacher_subject",
        "teacher_subject__subject",
    )

    serializer = BookingListSerializer(
        bookings,
        many=True
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )
    
    
@api_view(["GET"])
# @permission_classes([IsAuthenticated, IsTeacher])
def teacher_booking_detail(request, pk):

    booking = get_object_or_404(
        BookingRequest.objects.select_related(
            "student",
            "teacher_subject",
            "teacher_subject__subject",
        ),
        pk=pk,
        teacher_subject__teacher=request.user.teacher_profile
    )

    serializer = BookingDetailSerializer(
        booking
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )
    
    
@api_view(["PATCH"])
# @permission_classes([IsAuthenticated, IsTeacher])
def accept_booking(request, pk):

    booking = get_object_or_404(
        BookingRequest.objects.select_related(
            "teacher_subject"
        ),
        pk=pk,
        teacher_subject__teacher=request.user.teacher_profile
    )

    if booking.status != BookingStatus.PENDING:
        return Response(
            {
                "detail": "Cette demande a déjà été traitée."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    teacher_subject = booking.teacher_subject

    if not teacher_subject.is_active:
        return Response(
            {
                "detail": "Cette offre n'est plus active."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if teacher_subject.is_booked:
        return Response(
            {
                "detail": "Cette disponibilité est déjà réservée."
            },
            status=status.HTTP_409_CONFLICT
        )

    # Accepter la demande
    booking.status = BookingStatus.ACCEPTED
    booking.responded_at = timezone.now()
    booking.save(
        update_fields=[
            "status",
            "responded_at",
            "updated_at",
        ]
    )

    # La disponibilité devient réservée
    teacher_subject.is_booked = True
    teacher_subject.save(
        update_fields=[
            "is_booked",
            "updated_at",
        ]
    )

    # Les autres demandes en attente
    # pour cette même disponibilité sont refusées.
    BookingRequest.objects.filter(
        teacher_subject=teacher_subject,
        status=BookingStatus.PENDING
    ).exclude(
        pk=booking.pk
    ).update(
        status=BookingStatus.REJECTED,
        rejection_reason="La disponibilité a été attribuée à un autre étudiant.",
        responded_at=timezone.now()
    )

    message = f"votre demande pour le cours de {teacher_subject.subject.name} a ete accepte"
    create_notification(recipient=booking.student , notification_type="BOOKING_ACCEPTED" , title="Demande accepte" ,message=message)

    return Response(
        {
            "detail": "Demande acceptée avec succès."
        },
        status=status.HTTP_200_OK
    )
    
    
    
@api_view(["PATCH"])
# @permission_classes([IsAuthenticated, IsTeacher])
def reject_booking(request, pk):

    booking = get_object_or_404(
        BookingRequest,
        pk=pk,
        teacher_subject__teacher=request.user.teacher_profile
    )

    if booking.status != BookingStatus.PENDING:
        return Response(
            {
                "detail": "Cette demande a déjà été traitée."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    reason = request.data.get(
        "rejection_reason"
    )

    if not reason:
        return Response(
            {
                "detail": "Le motif du refus est obligatoire."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    booking.status = BookingStatus.REJECTED
    booking.rejection_reason = reason
    booking.responded_at = timezone.now()

    booking.save(
        update_fields=[
            "status",
            "rejection_reason",
            "responded_at",
            "updated_at",
        ]
    )
    message =( f"votre demande pour le cours de {booking.teacher_subject.subject.name} a ete refuse." f"Motif : {reason}" )
    create_notification(recipient=booking.student , notification_type="BOOKING_REJECTED" , title="Demande accepte" ,message=message)
    return Response(
        {
            "detail": "Demande refusée."
        },
        status=status.HTTP_200_OK
    )
    
    
    
    