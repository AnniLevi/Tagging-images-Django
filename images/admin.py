from django.contrib import admin

from images.models import Image, Tag


class TagAdminInline(admin.TabularInline):
    model = Tag


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "created_at")

    inlines = (TagAdminInline,)
