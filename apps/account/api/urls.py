from django.urls import path

from apps.account.api.views import UserRegisterAPI

name = "apps.account"

urlpatterns = [
    path("register", UserRegisterAPI.as_view(), name=name),
]
