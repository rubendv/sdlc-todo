"""Access-control tests for the User API (full permission stack)."""

from __future__ import annotations

import pytest
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from todo.users.adapters import DEFAULT_USER_GROUP
from todo.users.models import User
from todo.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db

LIST_URL = reverse("api:user-list")
ME_URL = reverse("api:user-me")


def _detail_url(user: User) -> str:
    return reverse("api:user-detail", kwargs={"username": user.username})


def _user(*, in_group: bool = True, **kwargs) -> User:
    user = UserFactory.create(**kwargs)
    if in_group:
        user.groups.add(Group.objects.get(name=DEFAULT_USER_GROUP))
    return user


def _client(user: User) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=user)
    return client


def test_anonymous_is_denied():
    # SR-1
    assert APIClient().get(LIST_URL).status_code in (
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    )


def test_list_is_scoped_to_self():
    # SR-6
    alice = _user()
    _user()  # a second user that must not appear
    response = _client(alice).get(LIST_URL)
    assert response.status_code == status.HTTP_200_OK
    assert [u["username"] for u in response.data] == [alice.username]


def test_can_retrieve_self():
    alice = _user()
    assert _client(alice).get(_detail_url(alice)).status_code == status.HTTP_200_OK


def test_cannot_retrieve_another_user():
    # SR-6: another user's record must be invisible
    alice, bob = _user(), _user()
    assert _client(alice).get(_detail_url(bob)).status_code == status.HTTP_404_NOT_FOUND


def test_missing_view_permission_is_forbidden():
    # SR-5
    user = _user(in_group=False)
    assert _client(user).get(ME_URL).status_code == status.HTTP_403_FORBIDDEN
    assert _client(user).get(_detail_url(user)).status_code == status.HTTP_403_FORBIDDEN


def test_can_update_self():
    alice = _user()
    response = _client(alice).patch(
        _detail_url(alice),
        {"name": "New Name"},
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    alice.refresh_from_db()
    assert alice.name == "New Name"


def test_cannot_escalate_privilege_via_patch():
    # SR-8: serializer does not expose privilege fields, so they are ignored.
    alice = _user()
    response = _client(alice).patch(
        _detail_url(alice),
        {"is_staff": True, "is_superuser": True},
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    alice.refresh_from_db()
    assert not alice.is_staff
    assert not alice.is_superuser


def test_self_delete_flushes_session():
    # FR-3 + self-delete logs the user out (session flushed).
    password = "sup3r-s3cret-pw"  # noqa: S105
    user = _user()
    user.set_password(password)
    user.save()

    client = APIClient()
    assert client.login(username=user.username, password=password)

    response = client.delete(_detail_url(user))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not User.objects.filter(pk=user.pk).exists()

    # Session was flushed: the next request is anonymous.
    assert client.get(ME_URL).status_code in (
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    )


def test_admin_has_no_api_bypass():
    # SR-9 / FR-6: superuser is own-record-only through the API.
    admin = UserFactory.create(is_staff=True, is_superuser=True)
    other = _user()
    client = _client(admin)

    listing = client.get(LIST_URL)
    assert listing.status_code == status.HTTP_200_OK
    assert [u["username"] for u in listing.data] == [admin.username]
    assert client.get(_detail_url(other)).status_code == status.HTTP_404_NOT_FOUND


def test_token_authentication_is_accepted():
    # FR-2: the API accepts token authentication.
    user = _user()
    token, _ = Token.objects.get_or_create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    response = client.get(ME_URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == user.username


def test_invalid_token_is_rejected():
    # FR-2 / SR-1: a bad token authenticates as nobody.
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token not-a-real-token")
    assert client.get(ME_URL).status_code in (
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    )
