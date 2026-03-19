from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ("username", "email", "role", "publisher", "is_staff")
    list_filter = ("role", "publisher", "is_staff", "is_active")

    fieldsets = UserAdmin.fieldsets + (
        (
            "Role Information",
            {
                "fields": (
                    "role",
                    "publisher",
                    "subscribed_publishers",
                    "subscribed_journalists",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Role Information",
            {
                "classes": ("wide",),
                "fields": ("role", "publisher"),
            },
        ),
    )