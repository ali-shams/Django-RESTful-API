from django.utils.translation import gettext_lazy as _
from django.db import (
    models,
    connection
)


class TimeStampMixin(models.Model):
    created = models.DateTimeField(
        _("created"),
        auto_now_add=True,
        help_text=_("Automatic registration of record creation time "
                    "in the database."),
    )
    modified = models.DateTimeField(
        _("modified"),
        auto_now=True,
        help_text=_("Automatic registration of record modification time "
                    "in the database."),
    )

    class Meta:
        abstract = True


class TruncateMixin:
    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE '{0}' CASCADE".format(cls._meta.db_table))  # noqa
