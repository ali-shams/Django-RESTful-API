from django.urls import path

from apps.account.api.views import (
    RegisterView,
    LoginView,
    LogoutView,
)

name = "apps.account"

urlpatterns = [
    path("register", RegisterView.as_view(), name=name),
    path("login", LoginView.as_view(), name=name),
    path('logout', LogoutView.as_view(), name='knox_logout')
]
