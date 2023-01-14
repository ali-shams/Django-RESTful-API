from django.db.models import QuerySet


class UserQuerySet(QuerySet):
    def set_user_verified(self, phone_number):
        self.filter(phone_number=phone_number).update(is_verified=True)

    def update_user_password(self, username, new_password):
        return self.filter(username=username).update(password=new_password)

    def find_user_by_phone_number(self, phone_number):
        return self.filter(phone_number=phone_number).first()
