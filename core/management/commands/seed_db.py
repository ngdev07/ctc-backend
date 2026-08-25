from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from academics.models import (
    Institution,
    Department,
    Level,
    Subject,
    ExamType,
)

from teachers.models import (
    TeacherProfile,
    TeacherSubject,
)

from students.models import StudentProfile

from bookings.models import (
    BookingRequest,
    BookingStatus,
)

from notifications.models import (
    Notification,
    NotificationType,
)


User = get_user_model()


class Command(BaseCommand):
    help = "Peuple la base de données avec des données de test."

    def handle(self, *args, **options):

        self.stdout.write(
            self.style.WARNING(
                "Création des données de test..."
            )
        )

        # ==================================================
        # 1. INSTITUTIONS
        # ==================================================

        institutions = {}

        institution_data = [
            {
                "name": "Université de Yaoundé I",
                "abbreviation": "UY1",
            },
            {
                "name": "Université de Douala",
                "abbreviation": "UD",
            },
        ]

        for data in institution_data:

            institution, _ = Institution.objects.get_or_create(
                abbreviation=data["abbreviation"],
                defaults={
                    "name": data["name"],
                },
            )

            institutions[
                institution.abbreviation
            ] = institution

        # ==================================================
        # 2. DEPARTMENTS
        # ==================================================

        departments = {}

        department_data = [
            {
                "institution": "UY1",
                "name": "Informatique",
                "abbreviation": "INFO",
            },
            {
                "institution": "UY1",
                "name": "Mathématiques",
                "abbreviation": "MATH",
            },
            {
                "institution": "UD",
                "name": "Génie Informatique",
                "abbreviation": "GI",
            },
        ]

        for data in department_data:

            department, _ = Department.objects.get_or_create(
                institution=institutions[
                    data["institution"]
                ],
                name=data["name"],
                defaults={
                    "abbreviation": data["abbreviation"],
                },
            )

            departments[
                data["abbreviation"]
            ] = department

        # ==================================================
        # 3. LEVELS
        # ==================================================

        levels = {}

        level_data = [
            ("Niveau 1", 1),
            ("Niveau 2", 2),
            ("Niveau 3", 3),
            ("Niveau 4", 4),
            ("Niveau 5", 5),
        ]

        for name, order in level_data:

            level, _ = Level.objects.get_or_create(
                name=name,
                defaults={
                    "order": order,
                },
            )

            levels[order] = level

        # ==================================================
        # 4. SUBJECTS
        # ==================================================

        subjects = {}

        subject_data = [
            ("Math 1", "MATH101", 1),
            ("Math 2", "MATH201", 2),
            ("Algorithme 1", "ALGO101", 1),
            ("Algorithme 2", "ALGO201", 2),
            ("Programmation 1", "PROG101", 1),
            ("Programmation 2", "PROG201", 2),
            ("Base de données 1", "BD101", 2),
            ("Réseaux 1", "RES101", 3),
            ("Systèmes d'exploitation", "SE301", 3),
            ("Intelligence artificielle", "IA401", 4),
        ]

        for name, code, level_order in subject_data:

            subject, _ = Subject.objects.get_or_create(
                code=code,
                defaults={
                    "name": name,
                    "level": levels[level_order],
                    "is_active": True,
                },
            )

            subjects[code] = subject

        # ==================================================
        # 5. EXAM TYPES
        # ==================================================

        exam_types = {}

        for name in [
            "CC",
            "Examen normal",
            "Rattrapage",
        ]:

            exam_type, _ = ExamType.objects.get_or_create(
                name=name
            )

            exam_types[name] = exam_type

        # ==================================================
        # 6. ADMIN
        # ==================================================

        admin, created = User.objects.get_or_create(
            email="admin@test.com",
            defaults={
                "username": "admin",
                "first_name": "Admin",
                "last_name": "Test",
                "role": User.Role.admin,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
                "is_verified": True,
                "is_email_verified": True,
            },
        )

        if created:
            admin.set_password("Admin12345!")
            admin.save()

        # ==================================================
        # 7. TEACHERS
        # ==================================================

        teachers = []

        teacher_data = [
            (
                "teacher1@test.com",
                "teacher1",
                "Jean",
                "Dupont",
                "UY1",
                "INFO",
            ),
            (
                "teacher2@test.com",
                "teacher2",
                "Paul",
                "Martin",
                "UY1",
                "MATH",
            ),
            (
                "teacher3@test.com",
                "teacher3",
                "Marc",
                "Ngono",
                "UD",
                "GI",
            ),
            (
                "teacher4@test.com",
                "teacher4",
                "David",
                "Mbarga",
                "UY1",
                "INFO",
            ),
            (
                "teacher5@test.com",
                "teacher5",
                "Eric",
                "Mballa",
                "UD",
                "GI",
            ),
        ]

        for (
            email,
            username,
            first_name,
            last_name,
            institution_code,
            department_code,
        ) in teacher_data:

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "role": User.Role.teacher,
                    "is_active": True,
                    "is_verified": True,
                    "is_email_verified": True,
                },
            )

            if created:
                user.set_password(
                    "Teacher12345!"
                )
                user.save()

            profile, _ = TeacherProfile.objects.get_or_create(
                user=user,
                defaults={
                    "institution": institutions[
                        institution_code
                    ],
                    "departement": departments[
                        department_code
                    ],
                    "bio": (
                        f"Professeur de "
                        f"{first_name} {last_name}."
                    ),
                    "experience_years": 3,
                    "average_rating": 4,
                    "total_reviews": 10,
                    "rating": 4,
                },
            )

            teachers.append(profile)

        # ==================================================
        # 8. STUDENTS
        # ==================================================

        students = []

        student_data = [
            (
                "student1@test.com",
                "student1",
                "Alice",
                "Martin",
                "UY1",
                "INFO",
                1,
            ),
            (
                "student2@test.com",
                "student2",
                "Kevin",
                "Ngono",
                "UY1",
                "INFO",
                2,
            ),
            (
                "student3@test.com",
                "student3",
                "Sarah",
                "Mballa",
                "UY1",
                "MATH",
                1,
            ),
            (
                "student4@test.com",
                "student4",
                "Paul",
                "Etoa",
                "UD",
                "GI",
                2,
            ),
            (
                "student5@test.com",
                "student5",
                "Chris",
                "Mekongo",
                "UD",
                "GI",
                3,
            ),
        ]

        for (
            email,
            username,
            first_name,
            last_name,
            institution_code,
            department_code,
            level_order,
        ) in student_data:

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "role": User.Role.student,
                    "is_active": True,
                    "is_verified": True,
                    "is_email_verified": True,
                },
            )

            if created:
                user.set_password(
                    "Student12345!"
                )
                user.save()

            profile, _ = StudentProfile.objects.get_or_create(
                user=user,
                defaults={
                    "institution": institutions[
                        institution_code
                    ],
                    "departement": departments[
                        department_code
                    ],
                    "level": levels[level_order],
                    "matricule": (
                        f"MAT{1000 + user.id}"
                    ),
                },
            )

            students.append(user)

        # ==================================================
        # 9. TEACHER SUBJECTS
        # ==================================================

        teacher_subjects = []

        assignments = [
            (0, "ALGO101", "CC", 5000, True),
            (0, "ALGO101", "Examen normal", 7000, True),
            (0, "PROG101", "CC", 5000, False),

            (1, "MATH101", "CC", 5000, True),
            (1, "MATH201", "Examen normal", 7500, True),

            (2, "PROG201", "CC", 6000, True),
            (2, "BD101", "Examen normal", 8000, True),

            (3, "ALGO201", "CC", 6000, True),
            (3, "RES101", "Examen normal", 7500, False),

            (4, "IA401", "Examen normal", 10000, True),
        ]

        for (
            teacher_index,
            subject_code,
            exam_name,
            price,
            is_primary,
        ) in assignments:

            teacher_subject, _ = (
                TeacherSubject.objects.get_or_create(
                    teacher=teachers[
                        teacher_index
                    ],
                    subject=subjects[
                        subject_code
                    ],
                    exam_type=exam_types[
                        exam_name
                    ],
                    defaults={
                        "price": Decimal(price),
                        "is_available": True,
                        "is_primary": is_primary,
                    },
                )
            )

            teacher_subjects.append(
                teacher_subject
            )

        # ==================================================
        # 10. BOOKINGS
        # ==================================================

        bookings = []

        if teacher_subjects and students:

            booking, _ = BookingRequest.objects.get_or_create(
                student=students[0],
                teacher_subject=teacher_subjects[0],
                defaults={
                    "proposed_price": Decimal("5000.00"),
                    "message": (
                        "Bonjour professeur, "
                        "je souhaite préparer mon CC."
                    ),
                    "status": BookingStatus.pending,
                },
            )

            bookings.append(booking)

        if len(students) > 1 and len(teacher_subjects) > 1:

            booking, _ = BookingRequest.objects.get_or_create(
                student=students[1],
                teacher_subject=teacher_subjects[1],
                defaults={
                    "proposed_price": Decimal("7000.00"),
                    "message": (
                        "Je souhaite préparer "
                        "mon examen."
                    ),
                    "status": BookingStatus.accepted,
                },
            )

            bookings.append(booking)

        if len(students) > 2 and len(teacher_subjects) > 2:

            booking, _ = BookingRequest.objects.get_or_create(
                student=students[2],
                teacher_subject=teacher_subjects[2],
                defaults={
                    "proposed_price": Decimal("5000.00"),
                    "message": (
                        "Je voudrais travailler "
                        "sur cette matière."
                    ),
                    "status": BookingStatus.rejected,
                    "rejection_reason": (
                        "Le créneau demandé "
                        "n'est plus disponible."
                    ),
                },
            )

            bookings.append(booking)

        # ==================================================
        # 11. NOTIFICATIONS
        # ==================================================

        if bookings:

            pending_booking = bookings[0]

            teacher_user = (
                pending_booking
                .teacher_subject
                .teacher
                .user
            )

            Notification.objects.get_or_create(
                recipient=teacher_user,
                notification_type=(
                    NotificationType.BOOKING_REQUEST
                ),
                title="Nouvelle demande de réservation",
                defaults={
                    "message": (
                        f"{pending_booking.student.get_full_name()} "
                        "vous a envoyé une demande."
                    ),
                    "is_read": False,
                },
            )

        if len(bookings) > 1:

            Notification.objects.get_or_create(
                recipient=bookings[1].student,
                notification_type=(
                    NotificationType.BOOKING_ACCEPTED
                ),
                title="Demande acceptée",
                defaults={
                    "message": (
                        "Votre demande de réservation "
                        "a été acceptée."
                    ),
                    "is_read": False,
                },
            )

        if len(bookings) > 2:

            Notification.objects.get_or_create(
                recipient=bookings[2].student,
                notification_type=(
                    NotificationType.BOOKING_REJECTED
                ),
                title="Demande refusée",
                defaults={
                    "message": (
                        "Votre demande de réservation "
                        "a été refusée."
                    ),
                    "is_read": False,
                },
            )

        # ==================================================
        # FIN
        # ==================================================

        self.stdout.write(
            self.style.SUCCESS(
                "\nBase de données remplie avec succès !"
            )
        )

        self.stdout.write(
            "\nComptes de test :"
        )

        self.stdout.write(
            "Admin    : admin@test.com / Admin12345!"
        )

        self.stdout.write(
            "Teachers : teacher1@test.com / Teacher12345!"
        )

        self.stdout.write(
            "Students : student1@test.com / Student12345!"
        )