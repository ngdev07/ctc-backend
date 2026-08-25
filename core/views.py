import json
from django.shortcuts import render

# =====================================================================
# FONCTION DE NETTOYAGE POUR JSON
# =====================================================================
def clean_for_json(obj):
    """
    Parcourt récursivement l'objet et convertit :
    - set → list
    - Ellipsis (...) → None
    - tout autre type non sérialisable sera converti en string
    """
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_for_json(v) for v in obj]
    elif obj is Ellipsis:
        return None   # ou return "..." si vous préférez
    else:
        return obj

# =====================================================================
# VUE PRINCIPALE
# =====================================================================
def api_home(request):
    endpoints = {
        # =============================================================
        # AUTHENTIFICATION
        # =============================================================
        "auth": [
            {
                "method": "POST",
                "path": "/api/accounts/login/",
                "description": "Connexion (email/password). Retourne des cookies HTTP-only.",
                "permission": "PUBLIC",
                "params": None,
                "body": {"email": "string", "password": "string"},
                "response": {
                    "message": "connexion reussie",
                    "user": {"id": 1, "username": "john", "role": "student"}
                }
            },
            {
                "method": "GET",
                "path": "/api/accounts/me/",
                "description": "Informations de l'utilisateur connecté.",
                "permission": "AUTHENTICATED",
                "params": None,
                "body": None,
                "response": {
                    "id": 1,
                    "username": "john",
                    "email": "john@example.com",
                    "first_name": "John",
                    "role": "student"
                }
            },
            {
                "method": "POST",
                "path": "/api/accounts/logout/",
                "description": "Déconnexion – supprime les cookies.",
                "permission": "AUTHENTICATED",
                "params": None,
                "body": None,
                "response": {"message": "Deconnexion reussie"}
            },
            {
                "method": "POST",
                "path": "/api/accounts/refresh/",
                "description": "Rafraîchir le token d'accès via le refresh token (cookie).",
                "permission": "PUBLIC",
                "params": None,
                "body": None,
                "response": {"message": "Access token renouvelle"}
            },
            {
                "method": "PATCH",
                "path": "/api/accounts/password/",
                "description": "Changer le mot de passe de l'utilisateur connecté.",
                "permission": "AUTHENTICATED",
                "params": None,
                "body": {
                    "old_password": "string",
                    "new_password": "string",
                    "confirm_password": "string"
                },
                "response": {"success": True, "message": "Mot de passe modifie avec success"}
            }
        ],

        # =============================================================
        # ACADEMICS – Institutions
        # =============================================================
        "academics-institutions": [
            {
                "method": "GET",
                "path": "/api/academics/institutions/",
                "description": "Liste des institutions.",
                "permission": "PUBLIC",
                "params": None,
                "body": None,
                "response": {
                    "count": 10,
                    "results": [{"id": 1, "name": "Université de Paris", "abbreviation": "UP"}]
                }
            }
        ],

        # =============================================================
        # ACADEMICS – Departments
        # =============================================================
        "academics-departments": [
            {
                "method": "GET",
                "path": "/api/academics/departments/",
                "description": "Liste des départements.",
                "permission": "PUBLIC",
                "params": None,
                "body": None,
                "response": {
                    "count": 5,
                    "results": [{"id": 1, "name": "Informatique", "institution": "Université de Paris"}]
                }
            }
        ],

        # =============================================================
        # ACADEMICS – Levels
        # =============================================================
        "academics-levels": [
            {
                "method": "GET",
                "path": "/api/academics/levels/",
                "description": "Liste des niveaux (Licence, Master...).",
                "permission": "PUBLIC",
                "params": None,
                "body": None,
                "response": {
                    "count": 3,
                    "results": [{"id": 1, "name": "Licence 1", "order": 1}]
                }
            }
        ],

        # =============================================================
        # ACADEMICS – Subjects
        # =============================================================
        "academics-subjects": [
            {
                "method": "GET",
                "path": "/api/academics/subjects/",
                "description": "Liste des matières.",
                "permission": "PUBLIC",
                "params": None,
                "body": None,
                "response": {
                    "count": 20,
                    "results": [{"id": 1, "name": "Mathématiques", "code": "MATH101", "level": "Licence 1"}]
                }
            }
        ],

        # =============================================================
        # ACADEMICS – Exam Types
        # =============================================================
        "academics-examtypes": [
            {
                "method": "GET",
                "path": "/api/academics/exam/",
                "description": "Liste des types d'examen.",
                "permission": "PUBLIC",
                "params": None,
                "body": None,
                "response": {
                    "count": 4,
                    "results": [{"id": 1, "name": "Contrôle continu"}]
                }
            }
        ],

        # =============================================================
        # TEACHERS
        # =============================================================
        "teachers": [
            {
                "method": "GET",
                "path": "/api/admin/teachers/",
                "description": "Liste des professeurs pour l'administration (filtres : search, department, is_active, ordering). Paginée.",
                "permission": "ADMIN",
                "params": {
                    "search": "string",
                    "department": "int",
                    "is_active": "bool",
                    "ordering": "string",
                    "page": "int",
                    "page_size": "int"
                },
                "body": None,
                "response": {
                    "count": 15,
                    "results": [{"id": 1, "full_name": "Jean Dupont", "email": "jean@example.com", "is_active": True}]
                }
            },
            {
                "method": "GET",
                "path": "/api/admin/teachers/<int:pk>/",
                "description": "Détail d'un professeur (admin).",
                "permission": "ADMIN",
                "params": None,
                "body": None,
                "response": {"id": 1, "full_name": "Jean Dupont", "email": "jean@example.com", "bio": "..."}
            },
            {
                "method": "PATCH",
                "path": "/api/admin/teachers/<int:pk>/suspend/",
                "description": "Suspendre un professeur.",
                "permission": "ADMIN",
                "params": None,
                "body": None,
                "response": {"success": True, "message": "Professeur suspendu avec succès."}
            },
            {
                "method": "PATCH",
                "path": "/api/admin/teachers/<int:pk>/activate/",
                "description": "Réactiver un professeur.",
                "permission": "ADMIN",
                "params": None,
                "body": None,
                "response": {"success": True, "message": "Professeur activé avec succès."}
            },
            {
                "method": "GET",
                "path": "/api/teachers/",
                "description": "Liste publique des professeurs actifs. Filtres : search, institution, department, min_reviews, min_average_rating, min_experience. Paginée.",
                "permission": "PUBLIC",
                "params": {
                    "search": "string",
                    "institution": "int",
                    "department": "int",
                    "min_reviews": "int",
                    "min_average_rating": "float",
                    "min_experience": "int",
                    "page": "int",
                    "page_size": "int"
                },
                "body": None,
                "response": {
                    "count": 10,
                    "results": [{"id": 1, "full_name": "Jean Dupont", "average_rating": 4.5}]
                }
            },
            {
                "method": "GET",
                "path": "/api/teachers/<int:pk>/",
                "description": "Détail public d'un professeur.",
                "permission": "PUBLIC",
                "params": None,
                "body": None,
                "response": {
                    "id": 1,
                    "full_name": "Jean Dupont",
                    "bio": "...",
                    "subjects": [{"id": 1, "subject_name": "Maths", "price": 30}]
                }
            },
            {
                "method": "GET",
                "path": "/api/teacher/profile/",
                "description": "Profil du professeur connecté.",
                "permission": "TEACHER",
                "params": None,
                "body": None,
                "response": {"id": 1, "full_name": "Jean Dupont", "bio": "...", "subjects": []}
            },
            {
                "method": "PATCH",
                "path": "/api/teacher/profile/",
                "description": "Modifier son profil professeur.",
                "permission": "TEACHER",
                "params": None,
                "body": {
                    "institution": "int",
                    "departement": "int",
                    "bio": "string",
                    "experience_years": "int"
                },
                "response": {"message": "Profil mis à jour avec succès.", "data": {}}
            },
            {
                "method": "GET",
                "path": "/api/teacher/subjects/",
                "description": "Liste des matières enseignées par le professeur connecté.",
                "permission": "TEACHER",
                "params": None,
                "body": None,
                "response": [{"id": 1, "subject_name": "Maths", "price": 30, "is_available": True}]
            },
            {
                "method": "POST",
                "path": "/api/teacher/subjects/",
                "description": "Ajouter une matière à son enseignement.",
                "permission": "TEACHER",
                "params": None,
                "body": {
                    "subject": "int",
                    "exam_type": "int",
                    "price": "decimal",
                    "is_available": "bool",
                    "is_primary": "bool"
                },
                "response": {"id": 1, "subject_name": "Maths", "price": 30}
            },
            {
                "method": "GET",
                "path": "/api/teacher/subjects/<int:pk>/",
                "description": "Détail d'une matière enseignée.",
                "permission": "TEACHER",
                "params": None,
                "body": None,
                "response": {"id": 1, "subject_name": "Maths", "price": 30}
            },
            {
                "method": "PATCH",
                "path": "/api/teacher/subjects/<int:pk>/",
                "description": "Modifier une matière enseignée.",
                "permission": "TEACHER",
                "params": None,
                "body": {"price": "decimal", "is_available": "bool"},
                "response": {"id": 1, "subject_name": "Maths", "price": 35}
            },
            {
                "method": "DELETE",
                "path": "/api/teacher/subjects/<int:pk>/",
                "description": "Supprimer une matière enseignée.",
                "permission": "TEACHER",
                "params": None,
                "body": None,
                "response": {"message": "Matière supprimée avec succès."}
            },
            {
                "method": "POST",
                "path": "/api/create/teachers/",
                "description": "Créer un compte professeur (admin).",
                "permission": "ADMIN",
                "params": None,
                "body": {"email": "string", "password": "string", "username": "string"},
                "response": {"success": True, "message": "Compte professeur créé avec succès", "data": {}}
            }
        ],

        # =============================================================
        # STUDENTS
        # =============================================================
        "students": [
            {
                "method": "GET",
                "path": "/api/admin/students/",
                "description": "Liste des étudiants pour l'administration. Filtres : search, institution, department, level, is_active. Paginée.",
                "permission": "ADMIN",
                "params": {
                    "search": "string",
                    "institution": "int",
                    "department": "int",
                    "level": "int",
                    "is_active": "bool",
                    "page": "int",
                    "page_size": "int"
                },
                "body": None,
                "response": {
                    "count": 30,
                    "results": [{"id": 1, "full_name": "Marie Martin", "email": "marie@example.com", "is_active": True}]
                }
            },
            {
                "method": "GET",
                "path": "/api/admin/students/<int:pk>/",
                "description": "Détail d'un étudiant (admin).",
                "permission": "ADMIN",
                "params": None,
                "body": None,
                "response": {"id": 1, "full_name": "Marie Martin", "email": "marie@example.com", "matricule": "1234"}
            },
            {
                "method": "PATCH",
                "path": "/api/admin/students/suspend/<int:pk>",
                "description": "Suspendre un étudiant.",
                "permission": "ADMIN",
                "params": None,
                "body": None,
                "response": {"message": "Étudiant suspendu avec succès."}
            },
            {
                "method": "PATCH",
                "path": "/api/admin/students/activate/<int:pk>",
                "description": "Réactiver un étudiant.",
                "permission": "ADMIN",
                "params": None,
                "body": None,
                "response": {"message": "Étudiant activé avec succès."}
            },
            {
                "method": "DELETE",
                "path": "/api/admin/students/delete/<int:pk>",
                "description": "Supprimer définitivement un étudiant.",
                "permission": "ADMIN",
                "params": None,
                "body": None,
                "response": {"message": "Étudiant supprimé avec succès."}
            },
            {
                "method": "GET",
                "path": "/api/students/",
                "description": "Liste publique des étudiants actifs. Filtres : search, institution, department, level. Paginée.",
                "permission": "PUBLIC",
                "params": {
                    "search": "string",
                    "institution": "int",
                    "department": "int",
                    "level": "int",
                    "page": "int",
                    "page_size": "int"
                },
                "body": None,
                "response": {
                    "count": 20,
                    "results": [{"id": 1, "full_name": "Marie Martin", "email": "marie@example.com"}]
                }
            },
            {
                "method": "GET",
                "path": "/api/students/<int:pk>/",
                "description": "Détail public d'un étudiant actif.",
                "permission": "PUBLIC",
                "params": None,
                "body": None,
                "response": {"id": 1, "full_name": "Marie Martin", "institution_name": "Université de Paris"}
            },
            {
                "method": "GET",
                "path": "/api/student/profile/",
                "description": "Profil de l'étudiant connecté.",
                "permission": "STUDENT",
                "params": None,
                "body": None,
                "response": {"id": 1, "full_name": "Marie Martin", "institution": 1, "level": 1}
            },
            {
                "method": "PATCH",
                "path": "/api/student/profile/",
                "description": "Modifier son profil étudiant.",
                "permission": "STUDENT",
                "params": None,
                "body": {
                    "institution": "int",
                    "departement": "int",
                    "level": "int",
                    "matricule": "string"
                },
                "response": {"message": "Profil mis à jour avec succès.", "data": {}}
            }
        ],

        # =============================================================
        # BOOKINGS
        # =============================================================
        "bookings": [
            {
                "method": "POST",
                "path": "/api/bookings/",
                "description": "Créer une demande de réservation (étudiant).",
                "permission": "STUDENT",
                "params": None,
                "body": {"teacher_subject": "int", "proposed_price": "decimal", "message": "string"},
                "response": {"id": 1, "status": "PENDING", "teacher": "Jean Dupont", "subject": "Maths"}
            },
            {
                "method": "GET",
                "path": "/api/bookings/my/",
                "description": "Liste des réservations de l'étudiant connecté.",
                "permission": "STUDENT",
                "params": None,
                "body": None,
                "response": [
                    {
                        "id": 1,
                        "teacher": "Jean Dupont",
                        "proposed_price": 30,
                        "status": "PENDING",
                        "created_at": "2025-01-01T10:00:00Z"
                    }
                ]
            },
            {
                "method": "GET",
                "path": "/api/bookings/<int:pk>/",
                "description": "Détail d'une réservation (étudiant).",
                "permission": "STUDENT",
                "params": None,
                "body": None,
                "response": {
                    "id": 1,
                    "student": "Marie Martin",
                    "teacher": "Jean Dupont",
                    "subject": "Maths",
                    "status": "PENDING"
                }
            },
            {
                "method": "PATCH",
                "path": "/api/bookings/<int:pk>/cancel/",
                "description": "Annuler une réservation en attente (étudiant).",
                "permission": "STUDENT",
                "params": None,
                "body": None,
                "response": {"detail": "Demande annulée avec succès."}
            },
            {
                "method": "GET",
                "path": "/api/bookings/teacher/",
                "description": "Liste des demandes reçues par le professeur connecté.",
                "permission": "TEACHER",
                "params": None,
                "body": None,
                "response": [
                    {"id": 1, "student": "Marie Martin", "proposed_price": 30, "status": "PENDING"}
                ]
            },
            {
                "method": "GET",
                "path": "/api/bookings/teacher/<int:pk>/",
                "description": "Détail d'une demande reçue (professeur).",
                "permission": "TEACHER",
                "params": None,
                "body": None,
                "response": {
                    "id": 1,
                    "student": "Marie Martin",
                    "teacher": "Jean Dupont",
                    "subject": "Maths",
                    "status": "PENDING"
                }
            },
            {
                "method": "PATCH",
                "path": "/api/bookings/teacher/<int:pk>/accept/",
                "description": "Accepter une demande (professeur).",
                "permission": "TEACHER",
                "params": None,
                "body": None,
                "response": {"detail": "Demande acceptée avec succès."}
            },
            {
                "method": "PATCH",
                "path": "/api/bookings/teacher/<int:pk>/reject/",
                "description": "Rejeter une demande (professeur) avec un motif.",
                "permission": "TEACHER",
                "params": None,
                "body": {"rejection_reason": "string"},
                "response": {"detail": "Demande refusée."}
            }
        ],

        # =============================================================
        # NOTIFICATIONS
        # =============================================================
        "notifications": [
            {
                "method": "GET",
                "path": "/api/notifications/",
                "description": "Liste des notifications de l'utilisateur connecté.",
                "permission": "AUTHENTICATED",
                "params": None,
                "body": None,
                "response": [
                    {
                        "id": 1,
                        "notification_type": "BOOKING_REQUEST",
                        "title": "Nouvelle demande",
                        "message": "...",
                        "is_read": False,
                        "created_at": "..."
                    }
                ]
            },
            {
                "method": "PATCH",
                "path": "/api/notifications/read/<int:pk>/",
                "description": "Marquer une notification comme lue.",
                "permission": "AUTHENTICATED",
                "params": None,
                "body": None,
                "response": {"detail": "Notification marquée comme lue."}
            },
            {
                "method": "PATCH",
                "path": "/api/notifications/read-all/",
                "description": "Marquer toutes les notifications comme lues.",
                "permission": "AUTHENTICATED",
                "params": None,
                "body": None,
                "response": {"detail": "Toutes les notifications sont marquées comme lues."}
            }
        ]
    }

    # === NETTOYAGE POUR JSON ===
    endpoints_clean = clean_for_json(endpoints)

    context = {
        "api_name": "Academic Tutoring API",
        "api_version": "v1",
        "description": "REST API for an academic tutoring platform",
        "endpoints_json": json.dumps(endpoints_clean),  # Maintenant sérialisable !
    }
    return render(request, "index.html", context)