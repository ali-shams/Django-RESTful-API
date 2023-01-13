from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import BaseUserManager

from apps.account.repository.queryset import UserQuerySet


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self,
                     username,
                     email,
                     password,
                     **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,
                    username,
                    email=None,
                    password=None,
                    **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self,
                         username,
                         email=None,
                         password=None,
                         **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, username):
        case_insensitive_username_field = "{}__iexact".format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def set_user_active(self, phone_number):
        return self.get_queryset().set_user_active(phone_number)

    def update_user_password(self, username, new_password):
        return self.get_queryset().update_user_password(username, new_password)


