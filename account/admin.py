from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission, User


class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "group_names",
        "is_staff",
    )

    def group_names(self, obj):
        return "\n".join([group.name for group in obj.groups.all()])


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Permission)
