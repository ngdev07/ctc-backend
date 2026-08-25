from django.urls import path

from .views import LoginView , MeView , LogoutView , RefreshView , changePassword

urlpatterns = [
    path("login/",LoginView.as_view(), name="login"),
    path("me/",MeView.as_view(), name="me"),
    path("logout/",LogoutView.as_view(), name="logout"),
    path("refresh/",RefreshView.as_view() , name="refresh"),
    path("password/" , changePassword , name="change_password")
]
