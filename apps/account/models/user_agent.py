from django.db import models
from django.utils.translation import gettext_lazy as _

from knox.models import AuthToken

class UserAgent(models.Model):
    user_agent = models.CharField(
        _("user agent"),
        unique=True,
        max_length=255,
        help_text=_("User agent"),
    )
    auth_token = models.OneToOneField(
        AuthToken,
        verbose_name=_('auth token'),
        related_name='user_agent',
        on_delete=models.PROTECT,
        help_text=_('The auth token this user agent belongs to')
    )

    class Meta:
        verbose_name = _("user agent")
        verbose_name_plural = _("user agents")

    def __str__(self):
        return f"{self.user_agent}"

    def __repr__(self):
        return f"{self.user_agent}"
