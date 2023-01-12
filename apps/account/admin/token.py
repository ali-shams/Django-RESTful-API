from django.contrib import admin

from apps.account.models import Token


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = (
        "token",
    )
    ordering = (
        "created",
    )
    readonly_fields = (
        "created",
        "modified"
    )
    save_on_top = True
