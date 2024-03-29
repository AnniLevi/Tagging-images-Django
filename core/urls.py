from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Tagging Images API",
        default_version="v1",
        description="""
        First training project
        Created by Anna Levitskaya
        """,
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

api_urls = [
    path("auth/", include("account.urls")),
    path("images/", include("images.urls")),
]

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("health-check/", include("health_check.urls")),
    path("admin/", admin.site.urls),
    path("api/", include(api_urls)),
]
