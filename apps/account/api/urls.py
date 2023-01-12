from knox import views as knox_views
from apps.account.api.views import LoginView
from django.urls import (
    path,
    re_path
)

from .views import (
    UserAPIView,
    ExampleView,
)

name = "apps.account"

urlpatterns = [
    path("", UserAPIView.as_view(), name=name),
    path("example/", ExampleView.as_view(), name=name),
]

urlpatterns.extend([
    re_path(r'`login`/', LoginView.as_view(), name='knox_login'),
    re_path(r'logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    re_path(r'logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
])
