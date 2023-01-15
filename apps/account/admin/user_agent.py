from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from knox.models import AuthToken

from apps.account.models import UserAgent


# class AuthTokenInLine(admin.TabularInline):
#     model = AuthToken
#     readonly_fields = (
#         "digest",
#         "created",
#         "token_key",
#         "expiry",
#     )
#     max_num = 0


@admin.register(UserAgent)
class UserAgentAdmin(admin.ModelAdmin):
    # inlines = (
    #     AuthTokenInLine,
    # )
    list_display = (
        "user_agent",
        "auth_token",
    )
    save_on_top = True
    fieldsets = [
        (_("Security Center"), {
            "classes": ("collapse",),
            "fields": (
                "user_agent",
                "auth_token",
            )
        })
    ]
