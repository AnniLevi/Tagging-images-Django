from django.urls import path

from . import views

urlpatterns = [
    path("", views.ImageView.as_view()),
    path("zip-upload/", views.ZipImageView.as_view()),
    path("tags/", views.TagView.as_view()),
]
