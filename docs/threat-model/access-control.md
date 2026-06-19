# Access Control

Mitigation for [open risk #1](stride-analysis.md). Design only — no implementation yet.

**Decision:** authorize with Django's built-in **model permission** system, plus object-level
ownership enforced in the API layer. No third-party authz (no django-guardian).

## Roles

| Role | Scope |
|------|-------|
| Anonymous | No API access (`IsAuthenticated` default) |
| User | CRUD on **own** user record and **own** tasks |
| Admin | Via API: **own objects only**, same as a user. Full access to all objects by other (non-API) means — mechanism TBD. |

## Why two layers

Django model permissions are **class-level** (`add/change/delete/view` per model). They answer
"can this user touch *Tasks* at all?" — they cannot express "*own* tasks". Both layers apply, and
**both must hold** (AND): the function-level permission is the primary gate, ownership only narrows it.

1. **Model permissions (function-level) — always enforced.** Every user is granted the Task and
   self-User CRUD perms via a default `users` group assigned at signup. DRF `DjangoModelPermissions`
   maps every HTTP verb → perm, **including `view_*` on reads**. If a user lacks the perm they are
   denied (403) — *even if they own the row*. Ownership never grants access; only the permission does.
2. **Object ownership (row-level) — narrows.** Restricts the granted verb to owned rows, in the view:
   - `get_queryset()` scopes to `request.user` — users never see others' rows.
   - `has_object_permission()` requires `obj.owner == request.user` — defense-in-depth against ID
     tampering even if the queryset is bypassed.

Order: the function-level permission is checked first; ownership is only evaluated for users who
already hold the perm.

**Admins get no API bypass.** Through the API the same function-level + ownership rules apply, so an
admin sees only their **own** objects, exactly like a user. A superuser does hold every model
permission (function-level), but the ownership layer still narrows the API to owned rows. Admins'
see-everything access is **out-of-band** — not through the API; mechanism TBD.

## Ownership

- **Task:** new model with `owner = FK(User)`. On create, `owner` is set **server-side** from
  `request.user` (never client-supplied).
- **Own user:** the requester's own `User` row. "CRUD" = read/update/delete self; **create = signup**
  (via allauth, not the authenticated API).

## Mass-assignment guard

Serializers must make `owner`, `is_staff`, `is_superuser`, `is_active`, and group/permission fields
**read-only via the API** (for everyone — privilege and ownership changes are not API operations).
Otherwise a user could reassign ownership or grant themselves privilege — Elevation (→ D1).

## DRF wiring (target)

- Default permission classes: `IsAuthenticated` + `DjangoModelPermissions` (subclassed to require
  `view_*` on GET/HEAD/OPTIONS — DRF's default leaves reads ungated) + `IsOwner` (object).
- Each viewset sets `queryset` (required by `DjangoModelPermissions`) and a per-user `get_queryset()`,
  applied to **all** authenticated users including admins (no superuser branch in the API).
- Read requires **both** the `view_*` permission (function-level) **and** ownership — a missing
  `view_*` perm is a 403 regardless of owner.

## Delta from scaffold

- `UserViewSet`: already scopes `get_queryset` to self ✅. Add `DjangoModelPermissions` + object perm;
  add account deletion (Destroy) for self-CRUD; keep create out (signup owns it).
- `TaskViewSet`: new — full CRUD, owner-scoped, `IsOwner`.
- Add default `users` group + perm assignment at signup (allauth adapter or post-migrate/data migration).
- Audit serializers for the mass-assignment guard above.

## Threat-model linkage

Closes open risk #1 and the access-control gaps in [STRIDE B1](stride-analysis.md):

- Tampering — BOLA via ID tampering → object ownership check (D1).
- Information disclosure — per-user `get_queryset` scoping (D1).
- Elevation — defined role model + mass-assignment guard (D1).

## To decide

- Admin out-of-band access mechanism (how admins see all objects without the API).
- Account self-deletion: hard vs soft delete (also a GDPR concern).
- Token lifecycle: per-user tokens; revoke on password change / logout.
