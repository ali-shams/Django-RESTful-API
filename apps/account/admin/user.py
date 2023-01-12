from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from knox.models import AuthToken

from apps.account.forms import UserCreationExtendedForm
from apps.account.models import User


class AuthTokenInLine(admin.TabularInline):
    model = AuthToken
    readonly_fields = (
        "digest",
        "created",
        "token_key",
        "expiry",
    )
    max_num = 0


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (
        AuthTokenInLine,
    )
    add_form = UserCreationExtendedForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "phone_number", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "phone_number",
        "is_verified",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "is_superuser",
        "is_verified",
    )
    search_fields = (
        "username",
        "phone_number",
    )
    search_help_text = "Search by username, and phone number."
    ordering = (
        "created",
    )
    readonly_fields = (
        "created",
        "modified",
    )
    save_on_top = True
    fieldsets = [
        (_("Basic Information"), {
            "fields": (
                "username",
                "email",
                "phone_number",
            )
        }),
        (_("Security Center"), {
            "classes": ("collapse",),
            "fields": (
                "password",
                "created",
                "modified"
            )
        })
    ]
