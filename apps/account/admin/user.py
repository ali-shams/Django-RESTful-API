from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.account.models import (
    User,
    Token
)


class TokenInLine(admin.TabularInline):
    model = Token
    fields = (
        'token',
    )
    readonly_fields = (
        'token',
    )
    extra = 0
    show_change_link = True


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = (
        TokenInLine,
    )
    list_display = (
        "username",
        "password",
        "phone_number",
    )
    list_filter = (
        "is_superuser",
        "is_staff",
        "is_active",
        "is_verified",
    )
    search_fields = (
        "username",
        "phone_number",
    )
    search_help_text = "you can look for users by username, and phone number."
    ordering = (
        "created",
    )
    readonly_fields = (
        "username",
        'created',
        'modified'
    )
    save_on_top = True
