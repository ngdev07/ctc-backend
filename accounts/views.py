from django.shortcuts import render
from django.contrib.auth import get_user_model , update_session_auth_hash
from django.db import transaction
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny , IsAuthenticated , IsAdminUser 
from rest_framework.decorators import api_view , permission_classes
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import UserSerializers
from .permissions import IsStudent , IsTeacher

from students.models import StudentProfile
User = get_user_model()

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self ,request):
        username = request.data.get("email")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {
                    "detail": "le username et le mot de passe sont requis"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request , username = username , password = password)

        if user is None:
            return Response(
                {
                    "details": "Identifiants Incorrects"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


        Refresh = RefreshToken.for_user(user)
        access = Refresh.access_token

        response = Response(
            {
                "message": "connexion reussie",
                "user": {
                    "id":user.id,
                    "username": user.username,
                    "role": user.role,
                }
            },
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="access_token",
            value = str(access),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=60*30,
        )

        response.set_cookie(
            key="refresh_token",
            value = str(access),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=60*60* 24 * 25,
        )


        return response





class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self , request):
        user = request.user 
        return Response({
            "id":user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "role": user.role,
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self , request):

        response = Response({
            "message" : "Deconnexion reussie"
        })

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response


class RefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self ,request):
   
        Refresh = request.COOKIES.get("refresh_token")

        if not Refresh:
            return Response({
                "detail": "Refresh token manquant" 
            }, 
            status= status.HTTP_401_UNAUTHORIZED)


        try:
            refresh = RefreshToken(Refresh)
            access_token = refresh.access_token

        except TokenError:
            return Response({
                "details": "Refresh token invalide ou expire" 
            },
             status= status.HTTP_401_UNAUTHORIZED)



        response = Response({
            "message":"Access token renouvelle"
        },
        status= status.HTTP_200_OK)

        response.set_cookie(
            key="access_token",
            value = str(access_token),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=60*30,
        )


        return response



@api_view(["POST"])
@permission_classes([AllowAny])
def student_register(request):

    email = request.data.get("email")
    password = request.data.get("password")
    username = request.data.get("username")
    first_name = request.data.get("first_name" , "")
    last_name = request.data.get("last_name" , "")


    if not email or not username or not password:
        return Response({
            "success": False,
            "message":(
                "Informations requises"
            )
        } , status= status.HTTP_400_BAD_REQUEST)


    if User.objects.filter(email__iexact = email).exists():
        return({
            "success": False,
            "message": "Cette adresse email est deja utilise",
        } ,  status.HTTP_409_CONFLICT)
    
    if User.objects.filter(username__iexact = username).exists():
            return({
                "success": False,
                "message": "Ce nom d'utilisateur est deja utilise",
            } ,  status.HTTP_409_CONFLICT)


    with transaction.atomic():

        user = User.objects.create_user(
            email=email,
            username= username,
            password=password,
            first_name = first_name,
            last_name = last_name,
            role =  'student',
        )

        StudentProfile.objects.create(user = user)

        return Response({
            "success": True,
            "message": "Compte etudiant crée avec succes",
            "data" : UserSerializers(user).data

        } ,  status.HTTP_201_CREATED)

    

@api_view(["PATCH"])
# @permission_classes([IsAuthenticated])
def changePassword(request):

    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")
    confirm_password = request.data.get("confirm_password")

    if not old_password or not new_password:
            return Response({
                "success": False,
                "message":(
                    "Informations requises"
                )
            } , status= status.HTTP_400_BAD_REQUEST)

    if not request.user.check_password(old_password):
        return Response({
            "success": False,
            "message": "Ancien mot de passe incorrect"
        } , status.HTTP_400_BAD_REQUEST)
    
    if not new_password != confirm_password:
            return Response({
                "success": False,
                "message": "les mots de passe ne correspondent pas"
            } , status.HTTP_400_BAD_REQUEST)


    request.user.set_password(new_password)
    request.user.save(update_fields = ["password"])

    update_session_auth_hash(request, request.user)


    return Response({
         "success" : True,
         "message" : "Mot de passe modifie avec success"
    } , status.HTTP_200_OK)