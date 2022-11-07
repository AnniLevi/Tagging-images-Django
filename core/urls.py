from django.contrib import admin
from django.urls import include, path

api_urls = [
    path("auth/", include("account.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urls)),
]
