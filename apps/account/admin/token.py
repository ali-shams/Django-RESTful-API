from django.contrib import admin

from apps.account.models import Token


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = (
        "token",
    )
    search_help_text = "you can look for token by user's phone number."
    ordering = (
        "created",
    )
    readonly_fields = (
        'created',
        'modified'
    )
    save_on_top = True
