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

## CWE coverage

The [CWE shortlist](../threat-model/attack-trees.md) and [secure coding guidelines](secure-coding-guidelines.md)
are enforced by a mix of tests, static analysis, and review. Authorization CWEs are business logic and
stay owned by tests + review; the mechanical ones are intended for SAST.

> **SAST is planned, not in place.** No proper SAST tool is set up yet — only a basic security linter
> (Ruff's `S` / Bandit rules) that catches a few of the mechanical items below. Until a real SAST tool
> and the custom rules exist (RR-2), every row relies on that linter, the tests, and manual review.

| CWE | Primary control |
|-----|-----------------|
| 639 / 862 — object-level authz | Custom SAST rules (owner-scoped `get_queryset`, `IsOwner` present) + negative tests (SR-6); residual logic to review |
| 285 / 863 — function-level authz | Custom SAST rules (no `AllowAny`, perms set) + tests (SR-5) |
| 915 — mass assignment | Tests (SR-8) + SAST (`fields = "__all__"`, missing `read_only`) |
| 200 / 209 — data/error exposure | Tests + review; SAST flags `DEBUG`, `__all__` serializers |
| 89 — SQL injection | SAST (raw / `.extra` / string SQL) + review |
| 79 — stored XSS | SAST (`mark_safe`, `\|safe`) + frontend review |
| 502 — deserialization | SAST (`pickle`, `yaml.load`) |
| 78 — command injection | SAST (`shell=True`, `os.system`) |
| 918 — SSRF | Review (no server-side fetch in MVP) |
| 287 / 384 / 613 — auth/session | Review (use allauth; no custom auth) |

## SAST requirements

A basic security linter (**Ruff's `S` / Bandit rules**) runs in pre-commit and catches a few mechanical
issues (e.g. `shell=True`, `pickle`) plus `detect-private-key`. That is **not** a proper SAST tool, and
we have **not set one up yet** (RR-2). The rest of this section is the requirements for the SAST tool we
will adopt; it must:

1. Be **Python + Django/DRF aware**, not generic Python only.
2. Detect the mechanical shortlist CWEs — 89, 79 (`mark_safe`), 502, 78, 915 (`fields="__all__"`) —
   plus `DEBUG=True` and `AllowAny`.
3. Support **custom rules**, to encode our conventions: a viewset must override an owner-scoped
   `get_queryset`; object views must set `IsOwner`; serializers must not use `__all__` and must mark
   privilege fields `read_only`. This is the only way SAST touches the authz CWEs.
4. Run **locally and in pre-commit**, failing on findings; wire into CI when one exists.
5. Allow **inline suppression with a written justification**, and keep false positives manageable.
6. Be **OSS / no paid license**, installed only with approval (project rule).

Once set up with **custom rules tailored to our app**, SAST would verify most of the authorization
conventions structurally: owner-scoped `get_queryset`, `IsOwner` on object views, no `fields="__all__"`,
privilege fields `read_only`, no `AllowAny` — covering the bulk of CWE-639/862/285/863 at the convention
level. None of that is built yet (RR-2); for now those conventions are held by the tests and review.

Even with custom rules, deeper semantic correctness — e.g. a `get_queryset` overridden but scoped to the
wrong field — would stay out of reach and on manual review.

Candidates to evaluate later (not a decision): **Semgrep** (Django/DRF rulesets + custom rules — meets
req 3), standalone **Bandit** (overlaps Ruff `S`), **CodeQL** (deep dataflow for 89 / 918).

## Test data

`factory-boy`: reuse `UserFactory` (exists); add `TaskFactory` (`owner = SubFactory(UserFactory)`).
Cross-user tests use two distinct users.

## Coverage bar

Every access-control SR has at least one positive **and** one negative test. No strict % gate this
iteration — depth on authorization over breadth.

## Out of scope (this iteration)

Production settings/hardening (TLS, HSTS, `DEBUG=False`), load/DoS (D3), audit/non-repudiation, MFA
enforcement, supply-chain test automation. Deferred with the [open risks](../threat-model/stride-analysis.md).
