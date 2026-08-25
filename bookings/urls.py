from django.urls import path

from .views import (
    create_booking,
    my_bookings,
    booking_detail,
    cancel_booking,

    teacher_bookings,
    teacher_booking_detail,
    accept_booking,
    reject_booking,
)


urlpatterns = [

    # ==========================
    # Étudiant
    # ==========================

    path(
        "",
        create_booking,
        name="create-booking",
    ),

    path(
        "my/",
        my_bookings,
        name="my-bookings",
    ),

    path(
        "<int:pk>/",
        booking_detail,
        name="booking-detail",
    ),

    path(
        "<int:pk>/cancel/",
        cancel_booking,
        name="cancel-booking",
    ),

    # ==========================
    # Professeur
    # ==========================

    path(
        "teacher/",
        teacher_bookings,
        name="teacher-bookings",
    ),

    path(
        "teacher/<int:pk>/",
        teacher_booking_detail,
        name="teacher-booking-detail",
    ),

    path(
        "teacher/<int:pk>/accept/",
        accept_booking,
        name="accept-booking",
    ),

    path(
        "teacher/<int:pk>/reject/",
        reject_booking,
        name="reject-booking",
    ),
]