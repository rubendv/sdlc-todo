# Todo

A small todo application built as a **reference implementation of a secure SDLC** — a software
development life cycle (the whole process of building software) with security designed in from the
first step instead of bolted on at the end. It is a worked example, not a product. The aim is for it
to eventually show what a well-developed SDLC looks like in practice.

> **Work in progress.** Built in roughly 8 hours on a free day. Local, debug-only, MVP core; not
> production-ready. The code and the correctness of the security analysis have **not** been thoroughly
> reviewed yet, and the writing still needs an editing pass to remove the "AI slop" feel. Treat it as
> an early first pass, not the finished example it is meant to become.

## What it does

A personal task tracker. A user can sign up (with email verification), log in and out, manage their
own account, and create, read, update, delete, and list their own tasks. A task is a title, an
optional description, and a done flag. Admins exist but get no special access through the API.

This is deliberately simple, not a complex real-world product. That is fine, because the goal is to
show the principles of a secure SDLC on something small enough to follow end to end. Those principles
scale to any size of organization. The wider point is that any company, a small startup included, can
stand up a secure SDLC incrementally rather than all at once, and that an LLM can speed the process up
if you work that way.

## New to secure development?

If you write software but have never watched someone "do security properly" from the start, this repo
is meant for you. The idea is simpler than the jargon makes it sound:

1. Decide what would be genuinely bad if it happened — user data leaking, the server getting taken
   over.
2. Work out how those things could happen.
3. Let that drive what you build, what you require, and what you test.
4. Write it down so it is a repeatable process, not something living in one person's head.

The rest of this README and the docs use security terms like *threat model*, *STRIDE*, and *CWE*.
Every one of them is defined in plain language in the [glossary](#jargon-in-plain-english) at the
bottom. Skim that first if a word trips you up.

## The story so far

The project is built in the order a secure SDLC runs, each step committed with its reasoning:

1. **Scaffold** — backend generated from cookiecutter-django, a project template that provides Django,
   a REST API, PostgreSQL, Redis, and login/accounts, on a Docker local-dev setup, in a monorepo with
   room for a frontend.
2. **Doomsday scenarios** — the three worst outcomes everything else is judged against: data
   disclosure, infrastructure abuse, and abandonment-level downtime.
3. **Model the system** — a context diagram and a data-flow diagram (pictures of how data moves) that
   mark the *trust boundaries*, the riskiest crossing points.
4. **Enumerate threats** — STRIDE (a checklist of threat types) on the outside edge, attack trees for
   the critical risks, and a shortlist of CWEs (standard coding-mistake categories) that matter here.
5. **Requirements and guidelines** — functional and security requirements, plus secure coding
   guidelines, each traced back to a specific threat.
6. **Build and prove it** — an access-controlled task and account API (users can only reach their own
   data), with tests for both what should work and what should be blocked, mapped to every requirement.
7. **Govern it** — deferred work recorded as accepted risks (known gaps with a condition for revisiting
   them), plus a SAMM assessment (a security-maturity self-check) and a short SDLC policy.

The [articles](docs/articles/) tell this as a narrative; the [docs](#explore-the-docs) hold the work.

## Status

Local, debug-only, MVP core. 54 tests passing. Deferred work is recorded as accepted risks with
review triggers, gated before any production deployment:

- Production settings and hardening (TLS, HSTS, secure cookies, `DEBUG=False`, production secrets).
- Denial-of-service mitigations and audit logging.
- A pass against ASVS v5 (a standard security checklist) and the Django deployment checklist.
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

## Jargon in plain English

The security terms used above, briefly.

- **SDLC (software development life cycle)** — the whole process of building software, from idea to
  running it. A *secure* SDLC builds security into every step instead of adding it at the end.
- **Threat model** — a structured look, done before building, at what could go wrong, who might cause
  it, and what you will do about it.
- **Doomsday scenario** — the worst outcomes the work exists to prevent. Here: leaking user data, the
  server being used to attack others, and downtime bad enough that users leave.
- **Data-flow diagram (DFD)** — a picture of how data moves between the parts of the system.
- **Trust boundary** — a line where data crosses from a less-trusted area into a more-trusted one (for
  example, the internet into your server). These crossings are where most risk lives.
- **STRIDE** — a checklist of six threat types (spoofing, tampering, repudiation, information
  disclosure, denial of service, elevation of privilege) used so no category is forgotten.
- **Attack tree** — a breakdown of the steps an attacker could chain together to reach a goal.
- **CWE (Common Weakness Enumeration)** — a standard catalog of coding-mistake types, such as SQL
  injection. We shortlist the ones most relevant to this app.
- **Access control / authorization** — deciding who may do what. *Object-level ownership* means a user
  can touch only their own records, not anyone else's.
- **Fail closed** — when the code is unsure, deny rather than allow.
- **CORS / same-origin** — browser rules about which websites may call your API. We sidestep the
  complexity by serving the frontend from the same address as the API.
- **Accepted risk / review trigger** — a gap we knowingly leave for now, written down with the
  condition that says when we must come back to it (often "before going to production").
- **SAST** — static analysis: tools that scan source code for likely security bugs.
- **SAMM (Software Assurance Maturity Model)** — a way to score how mature your security practices are
  and decide what to improve next.
- **ASVS (Application Security Verification Standard)** — a checklist of security requirements to test
  an application against.
