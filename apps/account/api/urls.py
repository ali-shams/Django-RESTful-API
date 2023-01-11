from django.urls import path
from .views import UserAPIView

name = "apps.account"

urlpatterns = [
    path("", UserAPIView.as_view(), name=name)
]
