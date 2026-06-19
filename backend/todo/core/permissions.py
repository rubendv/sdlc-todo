from __future__ import annotations

import logging

from django.contrib.auth import get_user_model
from rest_framework import permissions

logger = logging.getLogger(__name__)


class DjangoModelPermissionsStrict(permissions.DjangoModelPermissions):
    """``DjangoModelPermissions`` that also requires ``view_<model>`` for reads.

    DRF's default leaves GET/HEAD ungated. We require the view permission so a
    missing model permission is a 403 even for the object's owner (SR-5). OPTIONS
    stays open so DRF metadata is unaffected.
    """

    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": ["%(app_label)s.view_%(model_name)s"],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }


class IsOwner(permissions.BasePermission):
    """Object-level ownership.

    The owner is ``obj.owner`` (e.g. a Task) or ``obj`` itself (the User row).
    No admin bypass: admins are own-objects-only via the API (SR-9). This narrows
    the function-level model permission to owned rows (SR-6); it never grants.

    Fails closed: if the resolved owner is not a User instance, ownership is
    undefined and access is denied (and we log a warning, since it signals a
    misconfigured view).
    """

    def has_object_permission(self, request, view, obj) -> bool:
        owner = getattr(obj, "owner", obj)
        if not isinstance(owner, get_user_model()):
            logger.warning(
                "IsOwner denied: %s has no User owner; ownership is undefined",
                type(obj).__name__,
            )
            return False
        return owner == request.user
