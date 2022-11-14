from enum import Enum

from django.contrib.auth.models import Group


class UserGroups(Enum):
    user = 0
    verified_user = 1
    admin = 2


def create_groups():
    groups = [Group(name=g.name) for g in UserGroups]
    Group.objects.bulk_create(groups)


def check_user_group(user, levels_list):
    """Checks whether user is in the given group."""

    if not user.groups.filter(
        name__in=[UserGroups(l).name for l in levels_list]
    ).exists():
        return False
    return True
