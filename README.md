# Todo

I am a product security consultant. I created this repository to have a small, practical example of how to approach secure software development. Many developers are looking for practical advice or examples to form their mental model of how to accomplish pretty much anything in software development. This repo is my attempt to provide that for software security.

Before I switched to full-time security consulting, I worked as a software engineer on the backend of products where security was a major focus. This was before the time of AI coding. Creating this example application is also my way of familiarizing myself with the AI coding tools that are an important part of modern software development, so I do not end up as a dinosaur stuck in my old ways.

You will no doubt notice that much of the material in this repository is (co-)authored by an LLM. There is no vibe-coding happening here though. I have walked the LLM step by step through the activities of a proper secure software development lifecycle (SDLC), and have left the artifacts of each step visible in the [docs](/docs/) folder for you to look at.

Right now, I am going through the initial files that the LLM created when I started this project, and gradually reviewing things and rewriting bits in my voice instead of the LLM's. The thought-process and principles behind everything were provided by me, and not by the LLM.


> **Work in progress.** Built in roughly 8 hours on a free day. Local, debug-only, MVP core; not
> production-ready. The code and the correctness of the security analysis have **not** been thoroughly
> reviewed yet, and the writing still needs an editing pass to remove the "AI slop" feel. Treat it as
> an early first pass, not the finished example it is meant to become.

## What it does

A personal task tracker. A user can sign up (with email verification), log in and out, manage their
own account, and create, read, update, delete, and list their own tasks. A task is a title, an
optional description, and a done flag. Admins exist but get no special access through the API.

This is deliberately simple, not a complex real-world product. That is fine, because the goal is to
show the principles of a secure SDLC on something small enough to follow end to end.
I want to show that incorporating security into your SDLC doesn't need to be a costly and complex undertaking, all companies, tiny or huge, can do it.

## New to secure development?

If you write software but have never watched someone "do security properly" from the start, this repo
is meant for you. The basic process is simpler than the jargon makes it sound:

1. Decide what would be genuinely bad if it happened. For example: user data leaking, the server getting taken over. Everything we do in the SDLC must be there to prevent these things from happening.
2. Work out how these "doomsday scenarios" could happen. The steps that lead up to them, and the steps leading up to those steps.
3. Let that drive what kind of security protections you need, what you require, and what you test.
4. Write it down so it is a repeatable process, not something living in one person's head.

The rest of this README and the docs use security terms like *threat model*, *STRIDE*, and *CWE*.
Every one of them is defined in plain language in the [glossary](#jargon-in-plain-english) at the
bottom. Skim that first if a word trips you up.

## The steps we've gone through so far

An SDLC follows a certain natural order. I've chosen to start in a small, agile manner. We don't need everything perfect just yet, we need the ability to iterate fast, but still follow the secure development principles as we go along.

1. **Scaffold**: [backend](backend/) generated from cookiecutter-django, a project template that provides Django,
   a REST API, PostgreSQL, Redis, and login/accounts, on a Docker local-dev setup, in a monorepo with
   room for a frontend, to be added later. By using this scaffold, we already get a lot of best practices provided for free. We will still review this setup more deeply at a later time.
2. **[Doomsday scenarios](docs/threat-model/doomsday-scenarios.md)**: the three worst outcomes everything else is judged against: data
   disclosure, infrastructure abuse, and significant downtime.
3. **Model our system design**: a [context diagram](docs/threat-model/context-diagram.md) and a [data-flow diagram](docs/threat-model/level-1-dfd.md) (pictures of how data moves) that
   mark the *trust boundaries*, the riskiest crossing points.
4. **Enumerate threats** — [STRIDE](docs/threat-model/stride-analysis.md) (a checklist of threat types) on the outside edge, [attack trees](docs/threat-model/attack-trees.md) for
   the critical risks, and a shortlist of CWEs (standard coding-mistake categories) that matter for our app.
5. **Requirements and guidelines** — [functional](docs/requirements/functional-requirements.md) and [security requirements](docs/requirements/security-requirements.md), plus [secure coding
   guidelines](docs/requirements/secure-coding-guidelines.md), each traced back to a specific threat. We also create a [strategy for testing](docs/requirements/testing-strategy.md) each requirement.
6. **Build and prove it**: simple [REST API endpoints](backend/) to manage users and tasks, built according to our functional and security requirements and [access-control design](docs/threat-model/access-control.md). We also test the implementation according to our testing strategy, tracked in a [coverage matrix](docs/requirements/test-coverage.md).
7. **Govern the process and manage our risks**: Create a [SAMM assessment](docs/governance/samm-assessment.md) to measure how mature our SDLC is at this point, and decide where we need to be before production deployment can happen, captured in an [SDLC policy](docs/governance/sdlc-policy.md). We also clearly record any unmitigated risks that we will accept for now in a [risk register](docs/threat-model/risk-register.md).
8. **Map the compliance landscape**: work out which privacy and data-protection laws would apply (GDPR, UK GDPR, US state laws) and where the gaps are, in a [compliance doc](docs/governance/compliance.md) (not legal advice — to be reviewed by a professional before any real launch). We then fed that back into the rest: a general compliance risk in the [risk register](docs/threat-model/risk-register.md), an updated [SAMM assessment](docs/governance/samm-assessment.md), and a few compliance quick wins (data export, full erasure, cookie scope) folded into our [functional](docs/requirements/functional-requirements.md) and [security requirements](docs/requirements/security-requirements.md).

Dive straight into the [work documents](#explore-the-docs) that contain the results of each
activity so far. (Narrative articles are planned but not yet written.)

## Current focus 
In the current iteration we are aiming for:
- Minimal local debug setup and functional core of the backend API.
- Reviewing and rewriting LLM contributions.


## Future work
- Production settings and hardening (TLS, HSTS, secure cookies, `DEBUG=False`, production secrets).
- Denial-of-service mitigations and audit logging.
- A pass against ASVS v5 (a standard security checklist) and the Django deployment checklist.
- Compliance work before any real user data — privacy notice, data-subject rights (export/erasure),
  breach process, retention, DPIA — mapped in the [compliance landscape](docs/governance/compliance.md).
- The frontend.

## Explore the docs

The docs are the point of this repository.

- Threat model: [docs/threat-model/](docs/threat-model/README.md)
- Requirements: [docs/requirements/](docs/requirements/README.md)
- Governance: [docs/governance/](docs/governance/README.md)

## Layout

```
todo/
├── backend/                  Django project (API)
├── docs/                     threat model, requirements, governance
├── frontend/                 not started; will be served same-origin via the reverse proxy
├── docker-compose.local.yml
└── justfile
```

## Run locally

You don't need to run anything to learn from this repo — the docs are self-contained. If you want to
poke at the API, here's how. It's not really doing much yet, just a REST API backend.
Stay tuned until it has a proper frontend.
Needs Docker with the compose plugin.

```
docker compose -f docker-compose.local.yml up --build
# API at http://localhost:8000, captured email at http://localhost:8025

# run the test suite (from another shell)
docker compose -f docker-compose.local.yml run --rm django pytest
```

The `justfile` provides shortcuts like `just up` and `just pytest` if you have
[`just`](https://just.systems) installed.

## Jargon in plain English

The security terms used above, briefly.

- **SDLC (software development life cycle)** — the whole process of building software, from idea to
  running it. A *secure* SDLC builds security into every step instead of adding it at the end.
- **Threat model** — a structured look, done before building, at what could go wrong, who might cause
  it, and what you will do about it. See [docs/threat-model/](docs/threat-model/README.md).
- **Doomsday scenario** — the worst outcomes the work exists to prevent. Here: leaking user data, the
  server being used to attack others, and downtime bad enough that users leave. See
  [doomsday scenarios](docs/threat-model/doomsday-scenarios.md).
- **Data-flow diagram (DFD)** — a picture of how data moves between the parts of the system. See the
  [level-1 DFD](docs/threat-model/level-1-dfd.md).
- **Trust boundary** — a line where data crosses from a less-trusted area into a more-trusted one (for
  example, the internet into your server). These crossings are where most risk lives.
- **STRIDE** — a checklist of six threat types (spoofing, tampering, repudiation, information
  disclosure, denial of service, elevation of privilege) used so no category is forgotten. See the
  [STRIDE analysis](docs/threat-model/stride-analysis.md).
- **Attack tree** — a breakdown of the steps an attacker could chain together to reach a goal. See
  [attack trees](docs/threat-model/attack-trees.md).
- **CWE (Common Weakness Enumeration)** — a standard catalog of coding-mistake types, such as SQL
  injection. We shortlist the ones most relevant to this app.
- **Access control** — deciding who may do what, and on which objects.
- **Same-origin** — serving the frontend from the same address as the API, which avoids issues with the same origin policy of the browser.
- **Risk register** — the written record of gaps we knowingly leave for now, each with the condition
  that says when we must come back to it (often "before going to production"). See
  [risk register](docs/threat-model/risk-register.md).
- **SAMM (Software Assurance Maturity Model)** — a way to score how mature your security practices are
  and decide what to improve next. See the [SAMM assessment](docs/governance/samm-assessment.md).
- **ASVS (Application Security Verification Standard)** — a checklist of security requirements to test
  an application against.
- **GDPR / data-subject rights** — EU data-protection law; gives people rights over their personal
  data (to be informed, and to access, correct, delete, or export it). The UK and many US states have
  similar laws.
