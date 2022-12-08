from django.urls import path

from . import views

urlpatterns = [
    path("", views.ImageView.as_view(), name="images"),
    path("zip-upload/", views.ZipImageView.as_view(), name="upload_zip"),
    path("tags/", views.TagView.as_view(), name="tags"),
    path("common-tags/", views.ImageCommonTagsView.as_view(), name="common_tags"),
    path("most-tagged/", views.ImageFreqTaggedView.as_view(), name="most_tagged"),
]
