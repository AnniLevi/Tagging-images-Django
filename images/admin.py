from django.contrib import admin

from images.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user")
