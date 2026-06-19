# Todo

A small todo application built as a **reference implementation of a secure SDLC**: the security work
drives the design before any feature code is written. It is a worked example, not a product.

> **Work in progress.** Local, debug-only, MVP core. Not production-ready (see the
> [risk register](docs/threat-model/risk-register.md)). This is a first pass meant to show a worked
> example. The author still needs to review everything thoroughly and clean the "AI slop" feel out of
> the writing, especially in the documentation. It will be improved over time.

## Status

Done so far:

- Backend scaffolded with cookiecutter-django (Django 6.0, DRF, PostgreSQL, Redis, allauth/MFA,
  WhiteNoise, Mailpit) on a Docker local-dev setup.
- Threat model: doomsday scenarios, context and level-1 DFD with prioritized trust boundaries, STRIDE
  on the perimeter, attack trees, a CWE shortlist, and an access-control design.
- Requirements (functional + security), secure coding guidelines, a testing strategy, and a
  test-coverage matrix.
- Core implementation: a Task model and a locked-down Task/User API using Django model permissions
  plus object-level ownership. 54 tests, positive and negative, covering the access-control
  requirements.

Deferred (recorded as accepted risks with review triggers):

- Production settings and hardening (TLS, HSTS, secure cookies, `DEBUG=False`, production secrets).
- Denial-of-service mitigations and audit logging.
- A pass against ASVS v5 and the Django deployment checklist.
- The frontend.

## Layout

```
todo/
├── backend/                  Django project (API)
├── docs/                     threat model, requirements, articles
├── frontend/                 not started; will be served same-origin via the reverse proxy
├── docker-compose.local.yml
└── justfile
```

## Run locally

Needs Docker with the compose plugin.

```
docker compose -f docker-compose.local.yml up --build
# API at http://localhost:8000, captured email at http://localhost:8025
just pytest    # run the test suite
```

## Docs

- Threat model: [docs/threat-model/](docs/threat-model/README.md)
- Requirements: [docs/requirements/](docs/requirements/README.md)
- Governance: [docs/governance/](docs/governance/README.md)
- Articles: [docs/articles/](docs/articles/)

## Built with AI, steered by a human

This project was developed with an LLM coding agent (Claude Code) under close direction from the
author, a product security consultant. The agent did the typing; the author made the decisions.

How the steering worked:

- Ground rules up front: ask before installing anything, surface decisions instead of assuming them,
  and commit every step with a message explaining why. The git history reconstructs the whole build.
- Security before code: doomsday scenarios, then the threat model, then requirements and tests, then
  implementation against that written target.
- The author kept the calls that are hard to undo: what gets installed, what is in scope, and the
  security design. The agent's output was reviewed and corrected at every step.
- Corrections happened constantly, including during implementation: tightening the ownership check to
  fail closed, guarding the self-delete logout, dropping CORS in favor of same-origin serving, and
  requiring a test for the exact permission set a new user receives.

The prose here and in the docs is a first draft. The author still needs to edit it down and remove
the generated feel; treat it as a worked example in progress, not a finished write-up. The articles
in [docs/articles/](docs/articles/) describe the process in more detail.
