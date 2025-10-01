"""
URL configuration for the core project.

This file defines the root URL mappings for:
- Django admin
- Orders API
- Authentication (OIDC, Token, JWT)
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Django admin panel
    path("admin/", admin.site.urls),

    # Orders app API routes
    path("api/", include("orders.urls")),

    # OpenID Connect authentication routes
    path("oidc/", include("mozilla_django_oidc.urls")),

    # DRF Token authentication
    path("api-token-auth/", obtain_auth_token),

    # JWT authentication
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
