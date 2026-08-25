from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

admin.site.register(User)
# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     list_display =(
#         "id", "username" , "email" , "role" , "is_active" , "is_verified",
#     )

#     list_filter = (
#         "role" , "is_active" , "is_verified"
#      )

#     search_fields = (
#         "username" , "email" , "first_name" , "last_name",
#     )

