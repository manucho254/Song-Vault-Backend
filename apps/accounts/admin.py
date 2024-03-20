from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import User, UserMedia


class UserAdminManager(UserAdmin):
    """ custom user admin manager

    Args:
        UserAdmin (_type_): user admin model
    """

    model = User

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        ("Personal info", {"fields": ("username", "first_name", "last_name")}),
        ("Utility info", {"fields": ("is_artist", "email_verified")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_admin",
                    "is_staff",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                    "email_verified",
                    "is_artist",
                    "is_active",
                    "is_admin",
                    "is_staff",
                ),
            },
        ),
    )
    list_display = (
        "email",
        "last_name",
        "email_verified",
        "is_active",
        "is_admin",
        "is_staff",
    )
    list_filter = ("is_active", "is_admin", "is_staff")
    search_fields = ("first_name", "last_name")
    filter_horizontal = ()
    list_per_page = 20


admin.site.register(User, UserAdminManager)
admin.site.register(UserMedia)
