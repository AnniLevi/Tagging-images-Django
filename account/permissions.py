from enum import Enum
from typing import List

from django.contrib.auth.models import Group, User


class UserGroups(Enum):
    user = 0
    verified_user = 1
    admin = 2


def create_groups():
    """Creates Group objects with names from UserGroups enum."""
    groups: List[Group] = [Group(name=g.name) for g in UserGroups]
    Group.objects.bulk_create(groups)


def check_user_group(user: User, levels_list: list) -> bool:
    """Checks whether user is in the given list of group levels from UserGroups
    enum."""
    return user.groups.filter(
        name__in=[UserGroups(l).name for l in levels_list]
    ).exists()
