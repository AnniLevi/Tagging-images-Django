from django.contrib.auth.models import Group


def create_groups():
    user_group = Group.objects.get_or_create(name="User")[0]
    verified_user_group = Group.objects.get_or_create(name="Verified User")[0]
    admin_group = Group.objects.get_or_create(name="Admin")[0]


# user_group.permissions.set([permission_list])
# user_group.permissions.add(permission, permission, ...)
# user_group.permissions.remove(permission, permission, ...)
# user_group.permissions.clear()

# user.groups.add(user_group)
