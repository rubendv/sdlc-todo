# Todo

A small todo application built as a **reference implementation of a secure SDLC**: the security work
drives the design before any feature code is written. It is a worked example, not a product.

> **Work in progress.** Local, debug-only, MVP core; not production-ready. This is a first pass to
> show the approach. The writing still needs an editing pass to remove the "AI slop" feel, especially
> in the docs. It will improve over time.

## The story so far

The project is built in the order a secure SDLC runs, each step committed with its reasoning:

1. **Scaffold** — backend generated with cookiecutter-django (DRF, PostgreSQL, Redis, allauth/MFA) on
   a Docker local-dev setup, in a monorepo with room for a frontend.
2. **Doomsday scenarios** — the three worst outcomes everything else is judged against: data
   disclosure, infrastructure abuse, and abandonment-level downtime.
3. **Model the system** — context diagram and a level-1 data-flow diagram with prioritized trust
   boundaries.
4. **Enumerate threats** — STRIDE on the perimeter, attack trees for the critical risks, and a CWE
   shortlist tailored to this stack.
5. **Requirements and guidelines** — functional and security requirements, plus secure coding
   guidelines, each traced to a threat.
6. **Build and prove it** — an access-controlled Task/User API (Django model permissions plus
   object-level ownership), with positive and negative tests mapped to every requirement in a
   coverage matrix.
7. **Govern it** — deferred work recorded as accepted risks with review triggers, plus a SAMM
   assessment and an SDLC policy that make the process explicit.

The [articles](docs/articles/) tell this as a narrative; the [docs](#explore-the-docs) hold the work.

## Status

Local, debug-only, MVP core. 54 tests passing. Deferred work is recorded as accepted risks with
review triggers, gated before any production deployment:

- Production settings and hardening (TLS, HSTS, secure cookies, `DEBUG=False`, production secrets).
- Denial-of-service mitigations and audit logging.
- A pass against ASVS v5 and the Django deployment checklist.
- The frontend.

## Explore the docs

The docs are the point of this repository.

- Threat model: [docs/threat-model/](docs/threat-model/README.md)
- Requirements: [docs/requirements/](docs/requirements/README.md)
- Governance: [docs/governance/](docs/governance/README.md)
- Articles: [docs/articles/](docs/articles/)

## Layout

```
todo/
├── backend/                  Django project (API)
├── docs/                     threat model, requirements, governance, articles
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

## Built with AI, steered by a human

Developed with an LLM coding agent (Claude Code) under close direction from the author, a product
security consultant. The agent did the typing; the author made the decisions.

How the steering worked:

- Ground rules up front: ask before installing anything, surface decisions instead of assuming them,
  and commit every step with a message explaining why. The git history reconstructs the whole build.
- Security before code: doomsday scenarios, then the threat model, then requirements and tests, then
  implementation against that written target.
- The author kept the calls that are hard to undo: what gets installed, what is in scope, and the
  security design. The agent's output was reviewed and corrected at every step, including tightening
  the ownership check to fail closed, guarding the self-delete logout, and dropping CORS for
  same-origin serving.

The prose here and in the docs is a first draft, pending the author's editing pass.
