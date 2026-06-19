# Security Requirements (MVP)

Derived from the threat model. Each links to a [doomsday scenario](../threat-model/doomsday-scenarios.md)
(DDS) and/or [STRIDE](../threat-model/stride-analysis.md) entry. `scaffold ✅` = already provided by
cookiecutter-django. DoS and non-repudiation are out of scope this iteration (see
[README](README.md)).

## Authentication & identity

| ID | Requirement | Ref |
|----|-------------|-----|
| SR-1 | All API endpoints require authentication; no anonymous access. (scaffold ✅ `IsAuthenticated`) | B1 Spoofing → D1 |
| SR-2 | Passwords stored with Argon2. (scaffold ✅) | B1 Spoofing → D1 |
| SR-3 | Email verification mandatory before login. (scaffold ✅ allauth) | B1 Spoofing → D1 |
| SR-4 | Transport encrypted with TLS + HSTS in production; secure, HttpOnly cookies. (scaffold ✅) | B1 Info disclosure → D1 |

## Authorization (access control)

See [access-control.md](../threat-model/access-control.md).

| ID | Requirement | Ref |
|----|-------------|-----|
| SR-5 | Function-level model permissions enforced for **every** verb including `view`; users get CRUD perms via a default `users` group at signup. Missing perm → 403 regardless of ownership. | B1 Elevation → D1 |
| SR-6 | Object-level ownership: a user may access only objects they own, enforced by per-user `get_queryset()` **and** `has_object_permission()`. Function perm **and** ownership must both hold. | B1 Tampering / Info disclosure → D1 |
| SR-7 | `owner` is set server-side from the authenticated user; never client-supplied. | B1 Tampering → D1 |
| SR-8 | Mass-assignment guard: `owner`, `is_staff`, `is_superuser`, `is_active`, groups, and permissions are read-only via the API. | B1 Elevation → D1 |
| SR-9 | Admins have no API privilege bypass; via the API they are own-objects-only. | B1 Elevation → D1 |

## Input & data handling

| ID | Requirement | Ref |
|----|-------------|-----|
| SR-10 | All DB access via the ORM / parameterized queries; input validated by DRF serializers; no raw SQL. (scaffold ✅) | B1 Tampering → D1 |
| SR-11 | `DEBUG = False` in production; no verbose errors or stack traces exposed. (scaffold ✅) | B1 Info disclosure → D1 |
| SR-12 | CORS restricted to the API path and the trusted frontend origin(s). (scaffold ✅ path; origins TBD) | B1 Info disclosure → D1 |

## Secrets & supply chain

| ID | Requirement | Ref |
|----|-------------|-----|
| SR-13 | Secrets supplied via environment, never committed; production env files excluded from VCS; `SECRET_KEY` from env. (scaffold ✅) | B2 Info disclosure → D1 |
| SR-14 | Dependencies pinned and hash-verified via `uv.lock`. (scaffold ✅) | B2 Spoofing/Tampering → D2 |
| SR-15 | Build images exclude secrets and VCS (`.dockerignore` excludes `.envs/`, `.git`). (scaffold ✅) | B2 Info disclosure → D1 |
