# Testing Strategy (MVP)

Validate the [functional](functional-requirements.md) and [security](security-requirements.md)
requirements using the scaffold's test stack. **Security tests for access control are the priority**
— they are how we prove the threat-model mitigations hold. Negative tests carry the weight.

## Tooling (scaffold ✅)

- `pytest` + `pytest-django` (`--ds=config.settings.test`, `--reuse-db`), `pytest-sugar`.
- `factory-boy` for test data; tests live beside each app (`todo/<app>/tests/...`).
- DRF `APIClient` for API tests; `coverage` + `django_coverage_plugin`; `mypy` for types.
- Run: `just pytest` (→ `docker compose run --rm django pytest`).

## Levels

- **Unit** — Task model, serializers (mass-assignment), the `IsOwner` permission.
- **API / integration** — `APIClient` against the endpoints: auth, CRUD, and authorization. **The core.**
- No E2E/browser, no load tests (DoS out of scope).

## Functional coverage (FR)

| FR | Test focus |
|----|-----------|
| FR-1 / FR-2 | Register → email-verify → login/logout; session and token auth both work |
| FR-3 | Self view/update/delete account |
| FR-4 | Task create/read/update/delete as owner |
| FR-5 | List returns only the caller's tasks |
| FR-6 | Admin via API behaves as a normal user |

## Security coverage (SR) — priority, negative tests

Access-control SRs need explicit **negative** tests:

| SR | Test (expected) |
|----|-----------------|
| SR-1 | Unauthenticated request → 401/403 on every endpoint |
| SR-3 | Unverified-email account cannot log in |
| SR-5 | User lacking `view_task` gets 403 **on their own task**; same for add/change/delete |
| SR-6 | User A cannot read/update/delete User B's task (404/403); list excludes B's tasks |
| SR-7 | `POST`/`PATCH` with `owner` set to another user is ignored; `owner == request.user` |
| SR-8 | `PATCH` of `is_staff` / `is_superuser` / `owner` / groups is ignored (values unchanged) |
| SR-9 | Superuser via API sees only own objects (no bypass) |
| SR-12 | CORS rejects an untrusted origin |

Config-level SRs (SR-2, SR-10, SR-13–15) are provided by the scaffold; assert the key ones cheaply
via settings tests (e.g. Argon2 first hasher) rather than heavy unit tests. Tests run against the
debug/test settings — production SRs (SR-4, SR-11) are deferred.

## Test data

`factory-boy`: reuse `UserFactory` (exists); add `TaskFactory` (`owner = SubFactory(UserFactory)`).
Cross-user tests use two distinct users.

## Coverage bar

Every access-control SR has at least one positive **and** one negative test. No strict % gate this
iteration — depth on authorization over breadth.

## Out of scope (this iteration)

Production settings/hardening (TLS, HSTS, `DEBUG=False`), load/DoS (D3), audit/non-repudiation, MFA
enforcement, supply-chain test automation. Deferred with the [open risks](../threat-model/stride-analysis.md).
