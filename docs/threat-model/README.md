# Todo — Threat Model

High-level threat model, written before implementation so security shapes the design.

**Built iteratively.** We model the highest-risk areas first and expand coverage over time rather
than modeling everything up front. What is modeled so far is in the steps below; what is deliberately
not yet modeled is in the [backlog](#not-yet-modeled-backlog), to be filled in as the app grows. A
gap in the backlog means *not yet analyzed*, not *judged safe*.

## System context

- Backend: Django + DRF, PostgreSQL, Redis, behind Traefik/Nginx, in Docker.
- Auth: django-allauth (MFA available); DRF Session + Token; `IsAuthenticated` default.
- Frontend: separate lightweight client over the API, served same-origin via the reverse proxy
  (no CORS); added later.
- Data: identity (emails, password hashes, MFA secrets, tokens) and task content (titles,
  descriptions, due dates). Task content is sensitive — treat as personal data.
- Operator: small/solo, EU-based → GDPR applies.

## Steps

1. Doomsday scenarios — [doomsday-scenarios.md](doomsday-scenarios.md) *(done)*
2. Trust boundaries & data-flow — [context-diagram.md](context-diagram.md), [level-1-dfd.md](level-1-dfd.md) *(done)*
3. Threat enumeration — STRIDE / attack trees — [stride-analysis.md](stride-analysis.md), [attack-trees.md](attack-trees.md) *(perimeter STRIDE + critical-risk attack trees → CWE shortlist)*
4. Mitigations & controls — [access-control.md](access-control.md) *(in progress: access control / open risk #1)*
5. Residual risk & decisions — [risk-register.md](risk-register.md)

## Not yet modeled (backlog)

Areas intentionally left for later iterations. Roughly ordered by priority; most feed D1. Each is a
modeling gap to fill, not a judgment that the risk is absent.

- **Account recovery & email flows** — STRIDE + attack tree for password reset, email verification,
  and account enumeration (the prime account-takeover path). (D1)
- **Session & token lifecycle** — token expiry/rotation/revocation, session invalidation on
  password/MFA change, and the session-vs-token CSRF interaction. (D1)
- **Internal trust zones** — per-element STRIDE for the data stores and app processes, starting with
  the Redis session cache (write-through sessions) and PostgreSQL. (D1)
- **Admin out-of-band access** — model the "see everything" mechanism once it is decided
  (access-control → To decide). (D1)
- **Availability / DoS** — resource-exhaustion analysis; concrete first step: pagination + request
  limits. (D3)
- **Detection & response** — how each doomsday is detected and scoped (logging, monitoring,
  alerting); pairs with audit logging (RR-4).
- **Data lifecycle & privacy** — retention, erasure (GDPR), and backups (add backups to the DFD). (D1)
- **Assumptions & trust** — state what we trust (host/Docker daemon, package registry, email
  provider, reverse proxy) and add the host as a DFD element.
- **Dependency vulnerability monitoring** — known-CVE / SCA tracking to complement provenance
  (RR-9–RR-11). (D2)
- **Risk rating** — assign likelihood and impact (and a resulting priority) to the threats and the
  [risk register](risk-register.md) entries; they are currently unrated.

The current STRIDE covers only the two perimeter boundaries; the rest is backlog.
