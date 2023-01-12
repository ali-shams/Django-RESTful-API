from django.urls import path

from apps.account.api.views import (
    UserRegisterAPI,
    UserLoginAPI,
)

name = "apps.account"

urlpatterns = [
    path("register", UserRegisterAPI.as_view(), name=name),
    path("login", UserLoginAPI.as_view(), name=name),
]
