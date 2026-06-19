"""Access-control tests for the Task API.

Negative tests carry the weight here (testing-strategy.md): each maps to a
security requirement and a doomsday scenario.
"""

from __future__ import annotations

import pytest
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from todo.tasks.models import Task
from todo.tasks.tests.factories import TaskFactory
from todo.users.adapters import DEFAULT_USER_GROUP
from todo.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db

LIST_URL = reverse("api:task-list")


def _detail_url(task: Task) -> str:
    return reverse("api:task-detail", kwargs={"pk": task.pk})


def _user(*, in_group: bool = True):
    """A user, by default carrying the baseline `users` group permissions."""
    user = UserFactory.create()
    if in_group:
        user.groups.add(Group.objects.get(name=DEFAULT_USER_GROUP))
    return user


def _client(user) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=user)
    return client


def test_anonymous_is_denied():
    # SR-1
    response = APIClient().get(LIST_URL)
    assert response.status_code in (
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    )


def test_owner_can_create_and_list():
    # FR-4 / FR-5 happy path
    user = _user()
    client = _client(user)

    created = client.post(LIST_URL, {"title": "Buy milk"}, format="json")
    assert created.status_code == status.HTTP_201_CREATED
    assert created.data["owner"] == user.pk

    listing = client.get(LIST_URL)
    assert listing.status_code == status.HTTP_200_OK
    assert [t["title"] for t in listing.data] == ["Buy milk"]


def test_list_is_scoped_to_owner():
    # SR-6
    alice, bob = _user(), _user()
    TaskFactory.create(owner=alice, title="alice task")
    TaskFactory.create(owner=bob, title="bob task")

    response = _client(alice).get(LIST_URL)
    assert [t["title"] for t in response.data] == ["alice task"]


def test_cannot_reach_another_users_task():
    # SR-6 (BOLA): another user's object is invisible -> 404
    alice, bob = _user(), _user()
    bob_task = TaskFactory.create(owner=bob)
    client = _client(alice)

    assert client.get(_detail_url(bob_task)).status_code == status.HTTP_404_NOT_FOUND
    assert (
        client.patch(_detail_url(bob_task), {"title": "x"}, format="json").status_code
        == status.HTTP_404_NOT_FOUND
    )
    assert client.delete(_detail_url(bob_task)).status_code == status.HTTP_404_NOT_FOUND


def test_missing_view_permission_is_forbidden_even_for_owner():
    # SR-5: function-level permission always enforced; no group => no view_task
    user = _user(in_group=False)
    own_task = TaskFactory.create(owner=user)
    client = _client(user)

    assert client.get(LIST_URL).status_code == status.HTTP_403_FORBIDDEN
    assert client.get(_detail_url(own_task)).status_code == status.HTTP_403_FORBIDDEN


def test_owner_is_server_set_on_create():
    # SR-7: client-supplied owner is ignored
    user, other = _user(), _user()
    response = _client(user).post(
        LIST_URL,
        {"title": "t", "owner": other.pk},
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Task.objects.get(pk=response.data["id"]).owner == user


def test_owner_cannot_be_reassigned_via_patch():
    # SR-8: owner is read-only
    user, other = _user(), _user()
    task = TaskFactory.create(owner=user)

    response = _client(user).patch(
        _detail_url(task),
        {"owner": other.pk},
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    task.refresh_from_db()
    assert task.owner == user


def test_admin_has_no_api_bypass():
    # SR-9: superuser is own-objects-only through the API
    admin = UserFactory.create(is_staff=True, is_superuser=True)
    other = _user()
    other_task = TaskFactory.create(owner=other)
    client = _client(admin)

    listing = client.get(LIST_URL)
    assert listing.status_code == status.HTTP_200_OK
    assert listing.data == []
    assert client.get(_detail_url(other_task)).status_code == status.HTTP_404_NOT_FOUND


def test_owner_can_retrieve_own_task():
    # FR-4 retrieve
    user = _user()
    task = TaskFactory.create(owner=user, title="mine")
    response = _client(user).get(_detail_url(task))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "mine"


def test_owner_can_update_own_task():
    # FR-4 update
    user = _user()
    task = TaskFactory.create(owner=user, completed=False)
    response = _client(user).patch(
        _detail_url(task),
        {"title": "updated", "completed": True},
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    task.refresh_from_db()
    assert task.title == "updated"
    assert task.completed is True


def test_owner_can_delete_own_task():
    # FR-4 delete
    user = _user()
    task = TaskFactory.create(owner=user)
    response = _client(user).delete(_detail_url(task))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Task.objects.filter(pk=task.pk).exists()
