from django.db.models import QuerySet


class UserQuerySet(QuerySet):
    def set_user_active(self, phone_number):
        self.filter(phone_number=phone_number).update(is_verified=True)
