from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


urlpatterns = [
    re_path(r"refresh/?$", TokenRefreshView.as_view(), name="token_refresh"),
    re_path(r"login/?$", TokenObtainPairView.as_view(), name="login"),
]
