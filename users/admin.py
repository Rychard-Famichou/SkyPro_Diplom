from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "phone", "role", "is_active")
    search_fields = ("username", "email", "phone")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    fieldsets = UserAdmin.fieldsets + (("Дополнительная информация", {"fields": ("phone", "role", "image")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Дополнительная информация", {"fields": ("phone", "role", "image")}),)
