# Todo — Threat Model

High-level threat model, written before implementation so security shapes the design.

## System context

- Backend: Django + DRF, PostgreSQL, Redis, behind Traefik/Nginx, in Docker.
- Auth: django-allauth (MFA available); DRF Session + Token; `IsAuthenticated` default.
- Frontend: separate lightweight client over the API (CORS), added later.
- Data: identity (emails, password hashes, MFA secrets, tokens) and task content (titles,
  descriptions, due dates). Task content is sensitive — treat as personal data.
- Operator: small/solo, EU-based → GDPR applies.

## Steps

1. Doomsday scenarios — [doomsday-scenarios.md](doomsday-scenarios.md) *(done)*
2. Trust boundaries & data-flow — [context-diagram.md](context-diagram.md), [level-1-dfd.md](level-1-dfd.md) *(done)*
3. Threat enumeration — STRIDE / attack trees — [stride-analysis.md](stride-analysis.md) *(in progress: perimeter boundaries)*
4. Mitigations & controls
5. Residual risk & decisions
