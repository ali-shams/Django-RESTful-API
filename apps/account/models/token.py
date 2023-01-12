import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from painless.models import TimeStampMixin

class Token(TimeStampMixin):
    token = models.UUIDField(
        _("token"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
        max_length=255,
        help_text=_("User's token"),
    )
    # ############################### #
    #              FKs                #
    # ############################### #
    user = models.ForeignKey(
         settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        related_name="tokens",
        null=True,
        on_delete=models.CASCADE,
        help_text=_("Access to the related user of a token"),
    )

    class Meta:
        verbose_name = _("token")
        verbose_name_plural = _("tokens")

    def __str__(self):
        return f"{self.token}"

    def __repr__(self):
        return f"{self.token}"
