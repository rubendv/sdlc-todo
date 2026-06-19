"""The default `users` group must grant exactly the baseline permissions (SR-5)."""

from __future__ import annotations

import pytest
from django.contrib.auth.models import Group

from todo.users.adapters import DEFAULT_USER_GROUP
from todo.users.adapters import add_to_default_group
from todo.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db

# CRUD on own tasks + self-account CRUD. No add_user (signup), no privilege perms.
EXPECTED_PERMISSIONS = {
    "tasks.add_task",
    "tasks.change_task",
    "tasks.delete_task",
    "tasks.view_task",
    "users.view_user",
    "users.change_user",
    "users.delete_user",
}


def _labels(perms) -> set[str]:
    return {f"{p.content_type.app_label}.{p.codename}" for p in perms}


def test_default_group_has_expected_permissions():
    group = Group.objects.get(name=DEFAULT_USER_GROUP)
    perms = group.permissions.select_related("content_type")
    assert _labels(perms) == EXPECTED_PERMISSIONS


def test_new_user_receives_exactly_expected_permissions():
    user = UserFactory.create()
    assert user.get_all_permissions() == set()  # nothing before joining the group

    add_to_default_group(user)

    # Refetch to avoid the cached permission set on the in-memory instance.
    user = type(user).objects.get(pk=user.pk)
    assert user.get_all_permissions() == EXPECTED_PERMISSIONS
