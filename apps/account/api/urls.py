from django.urls import path

from apps.account.api.views import (
    RegisterView,
    LoginView,
    LogoutView,
    SendOTPView,
    ValidateOTPView,
    ChangePassPView,
    ForgotPassPView,
    ListTokensView,
    KillTokensView,
)

name = "apps.account"

urlpatterns = [
    path("register", RegisterView.as_view(), name=name),
    path("login", LoginView.as_view(), name=name),
    path('logout', LogoutView.as_view(), name='knox_logout'),
    path('send-otp', SendOTPView.as_view(), name='name'),
    path('validate-otp', ValidateOTPView.as_view(), name='name'),
    path('change-pass', ChangePassPView.as_view(), name='name'),
    path('forgot-pass', ForgotPassPView.as_view(), name='name'),
    path('list-tokens', ListTokensView.as_view(), name='name'),
    path('kill-tokens', KillTokensView.as_view(), name='name'),
]
