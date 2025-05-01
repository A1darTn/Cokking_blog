from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import SwaggerApiDoc

schema_view = get_schema_view(
    openapi.Info(
        title="Swagger",
        default_version="v 0.0.1",
        description="Документация по API к ресурсу кулинария",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
)

urlpatterns = [
    path("swagger_ui/", SwaggerApiDoc.as_view(), name="swagger-ui"),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=1),
        name="schema-json",
    ),
]
