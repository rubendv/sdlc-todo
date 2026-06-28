# AGENTS.md

Guidance for AI coding agents (and humans pairing with them) working in this repository.

This repo is a **worked example of a secure SDLC**, not just an app. The code exists to make the
security process concrete; the docs are the point. Keep that in mind: a change to the code often
implies a change to the threat model, requirements, or test-coverage matrix, not just the code.

Start by reading [README.md](README.md) (especially "Start here" and "The steps we've gone through
so far") before touching anything.

## What this repo is (and isn't)

- **Is:** a deliberately small Django/DRF todo API used to demonstrate threat-modeling → requirements
  → implementation → testing → governance, end to end.
- **Is not:** production-ready, a crypto/pentest course, or legal advice. It runs local, debug-only.
  See the "Work in progress" note in the README and the [risk register](docs/threat-model/risk-register.md).
- **Scope now:** local, debug-enabled core. Production hardening, DoS mitigations, audit logging,
  MFA enforcement, and a frontend are deliberately deferred — each written down as an accepted risk
  with a review trigger, not silently missing.

If a task would push something into "production" territory (TLS, `DEBUG=False`, prod secrets,
deploying), stop and surface it as a decision rather than doing it. These are owner calls.

## How to work here

1. **Make the threat model drive the work.** Every control traces back to a [doomsday scenario]
   (docs/threat-model/doomsday-scenarios.md) and a [STRIDE](docs/threat-model/stride-analysis.md)
   entry. If you can't trace a change to one, ask before proceeding.
2. **Ask, don't assume, on product/risk decisions.** Roles, who-can-do-what, what is in/out of scope,
   compliance obligations — these are the owner's calls, not yours. Surface decisions, don't silently
   pick one.
3. **Keep the docs in sync with the code.** New requirement → add to
   [functional](docs/requirements/functional-requirements.md) or
   [security](docs/requirements/security-requirements.md) requirements and the
   [coverage matrix](docs/requirements/test-coverage.md). New threat → update the
   [threat model](docs/threat-model/README.md) and, if accepted-for-now, the
   [risk register](docs/threat-model/risk-register.md) with a rationale and a review trigger.
4. **Commit in small pieces with the reason in the message**, the way the repo already does. The
   history is meant to be readable as a narrative.
5. **No vibe-coding.** Walk step by step through the SDLC activity; leave the artifact of each step
   visible under `docs/`. Several docs carry an `> **Example prompt:**` block at the top showing how
   they were generated — follow that pattern for new docs.

## Repository layout

```
todo/
├── README.md                 start here; the SDLC steps; glossary
├── AGENTS.md                 this file
├── justfile                   shortcuts: just up / just pytest / just manage …
├── docker-compose.local.yml   local dev stack (Django + Postgres + Mailpit)
├── docs/                      the point of the repo
│   ├── threat-model/          doomsday scenarios, context/DFD, STRIDE, attack trees,
│   │                          access-control design, risk register
│   ├── requirements/          functional + security requirements, secure-coding guidelines,
│   │                          testing strategy, test-coverage matrix
│   ├── governance/            SAMM assessment, SDLC policy, compliance landscape
└── backend/                   Django project (the actual API)
    ├── config/                project settings (base/local/test/production), urls, api_router
    ├── todo/
    │   ├── core/permissions.py   DjangoModelPermissionsStrict + IsOwner (access-control core)
    │   ├── users/                custom User model, allauth adapters, API + admin + tests
    │   ├── tasks/                Task model + API + tests
    │   └── contrib/sites/        local sites migration override
    ├── tests/                  project-level tests
    ├── compose/                Docker images for local + production
    └── pyproject.toml          ruff, mypy, djlint, pytest config
```

## Running things

Everything runs through Docker Compose. [`just`](https://just.systems) is the convenient wrapper.

```bash
just up                 # start the stack (or: docker compose -f docker-compose.local.yml up -d)
just pytest             # run the test suite (or: docker compose -f docker-compose.local.yml run --rm django pytest)
just manage migrate     # any manage.py command
just logs django        # tail logs
just down               # stop (just prune to also drop volumes)
```

Services when up: API at http://localhost:8000, captured email (Mailpit) at http://localhost:8025.
Postgres and Mailpit are dependencies of `django`. There is **no frontend yet** — it is REST only.

Do **not** try to run Django directly on the host; the stack expects the container (Postgres host,
env files under `backend/.envs/.local/`). The local settings hardcode a dev `SECRET_KEY` and
`DEBUG=True` — local only, never deploy as-is.

## Tech stack (quick reference)

- **Python 3.14**, **Django 6**, **Django REST Framework**, managed with **uv** (lockfile
  `backend/uv.lock`, dependencies are hash-pinned — keep them pinned).
- **django-allauth** for accounts/signup/email-verification/MFA; DRF Session + Token auth.
- **PostgreSQL 18**, **Redis** (cache, configured but unused in MVP), **Mailpit** (local mail sink).
- **drf-spectacular** for OpenAPI at `/api/schema/` and `/api/docs/` (admin-only).
- **ruff** (lint+format), **mypy** (django-stubs), **djlint** (Django templates), **pytest** +
  **pytest-django** + **factory-boy**. **pre-commit** runs ruff, django-upgrade, djlint,
  pyproject-fmt, and secret detection (`detect-private-key`).

## Code conventions

- Follow what's already there. The codebase is deliberately terse and technical; don't pad.
- **Access control is the heart of this app.** Read
  [docs/threat-model/access-control.md](docs/threat-model/access-control.md) and
  [docs/requirements/secure-coding-guidelines.md](docs/requirements/secure-coding-guidelines.md)
  before writing any view or serializer. In particular:
  - Every viewset scopes `get_queryset()` to `request.user` — never return a global queryset.
  - Object endpoints must also use `IsOwner` (`has_object_permission`); the queryset is defense-in-depth,
    not the only check.
  - `owner` is set server-side in `perform_create()` from `request.user`, never from request data.
  - Serializers list fields explicitly (never `fields = "__all__"`); `owner`, `is_staff`,
    `is_superuser`, `is_active`, `groups`, `user_permissions` are read-only.
  - No admin bypass through the API. Admins are own-objects-only via the API, like any user.
  - Fail closed: when ownership is undefined, deny (see `IsOwner`, which logs a warning).
  - No CORS. The frontend will be served same-origin via the reverse proxy. Do not re-add
    `corsheaders`.
- Use the ORM; no `.raw()`/`.extra()`/string-built SQL.
- `from __future__ import annotations` is used throughout; keep that style.
- Ruff's config selects a broad rule set (incl. `S` for security, `DJ` for Django, `PT` for pytest).
  Don't disable rules without a stated reason in a comment.

## Testing conventions

- Tests live next to the code under `todo/<app>/tests/` (mirroring the app structure) plus
  `backend/tests/` for project-level concerns.
- The **negative tests carry the weight** — "the forbidden action must fail" is the core of the
  security suite (e.g. user A cannot reach user B's task; a missing `view` perm is 403 even for the
  owner; a client-supplied `owner` is ignored; an admin gets no API bypass).
- Keep the [test-coverage matrix](docs/requirements/test-coverage.md) accurate: every requirement
  maps to its positive (P) and negative (N) tests. When you add or change a requirement, update the
  matrix in the same change.
- Factories live in `todo/<app>/tests/factories.py` (`UserFactory`, etc.). Prefer factories over raw
  ORM in tests.
- Auth flows (signup, email verification, login/logout) currently lean on django-allauth's upstream
  tests rather than our own — this is a **recorded accepted risk (RR-1)**, to be remediated before
  production. Don't extend or customize those flows without also adding our own tests and revisiting
  the risk.

## Doc conventions

- Markdown only. Each work doc under `docs/` that was LLM-generated carries an
  `> **Example prompt:**` block at the top describing its inputs and the shape of its output, plus the
  standing instruction "ask me about product/risk decisions; don't assume." New docs should follow
  this so the work stays reproducible and teachable.
- Security terms are defined in the README [glossary](README.md#jargon-in-plain-english); use them
  consistently (CWE IDs, STRIDE categories, doomsday-scenario IDs like D1/D2/D3, requirement IDs like
  SR-5, risk IDs like RR-1).
- Narrative articles under `docs/articles/` are planned but not yet written. Do not flesh them out
  into finished prose without explicit instruction.
- The risk register is a table; direct (attacker) risks are phrased like the STRIDE analysis, and
  process/coverage gaps are phrased as "because <control> is missing, …". Follow that when adding rows.

## Guardrails (do not cross without asking)

- **Don't deploy or add production settings.** TLS/HSTS/secure cookies/`DEBUG=False`/prod secrets are
  gated behind the before-production risk triggers.
- **Don't add, remove, or broaden permissions** in the access-control design without owner sign-off and
  a doc update.
- **Don't introduce new dependencies** without hash-pinning in `uv.lock` and a stated reason; the
  supply-chain risks (RR-9 through RR-12) are deliberately tracked.
- **Don't add CORS**, analytics/tracking cookies, or anything that expands the data footprint without
  checking the [compliance doc](docs/governance/compliance.md) (GDPR is in scope for the operator).
- **Don't mark a risk "resolved"** in the risk register without the corresponding control being built
  and tested; risks are accepted with a trigger, not hand-waved away.

## When in doubt

Ask. This repo's whole point is that decisions with no stated basis are the ones that need the closest
look. State your reasoning, point at a specific threat or requirement, and let the owner make the calls
that are hard to undo (what gets installed, what gets shipped, what stays in scope).
