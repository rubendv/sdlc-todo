# STRIDE — perimeter boundaries

Initial STRIDE for the two **High-priority** boundaries from the [Level 1 DFD](level-1-dfd.md):
B1 Internet ↔ edge, and B2 build/deploy. Internal boundaries are out of scope here
(defense-in-depth, lower priority).

Risks are kept generic — *An attacker could `<action>` in order to `<goal>`, leading to
`<impact>`* — and each links to a [doomsday scenario](doomsday-scenarios.md) (DDS): **D1** disclosure,
**D2** infra/lateral movement, **D3** downtime. A risk with no DDS path is out of scope.

Mitigation status reflects what the cookiecutter-django scaffold already provides:
**Handled** · **Partial** (some coverage, gap remains) · **Open** (not handled) · **N/A yet**.

## B1 — Internet ↔ edge (API perimeter)

| STRIDE | Risk | Mitigation | DDS |
|--------|------|------------|-----|
| Spoofing | An attacker could impersonate a legitimate user in order to act on their behalf, leading to exposure of that user's data. | **Partial** — allauth auth flows + mandatory email verification, Argon2 hashing, secure/HttpOnly cookies, TLS+HSTS, default allauth login rate-limits. *Open: MFA not enforced; no throttling on API/token auth.* | D1 |
| Tampering | An attacker could manipulate requests or stored data in order to subvert intended behavior, leading to unauthorized access to data. | **Partial** — ORM (parameterized queries), CSRF protection, DRF serializer validation, TLS. *Open: object-level authorization — access-control architecture undecided.* | D1 (→ D2 if it yields system control) |
| Repudiation | An attacker could act without leaving a reliable trace in order to conceal their activity, leading to a breach that cannot be detected or scoped. | **Open** — only basic request/error logging; no audit trail of user/admin actions (Sentry off). | D1 |
| Information disclosure | An attacker could obtain data they are not authorized to see in order to harvest sensitive information, leading to exposure of user data. | **Partial** — DEBUG off in prod, `IsAuthenticated` default, CORS scoped to `/api/`, TLS. *Open: per-user query scoping / object-level authorization undecided.* | D1 |
| Denial of service | An attacker could exhaust system resources in order to make the service unavailable, leading to downtime that drives users away. | **Open** — no app-level throttling/rate limits or resource quotas. | D3 |
| Elevation of privilege | An attacker could gain more privilege than intended in order to bypass access controls, leading to broad access to user data. | **Partial** — `SECRET_KEY` via env, randomized admin URL, DEBUG off, `IsAuthenticated` default. *Open: authorization/role model undecided.* | D1 (→ D2 if it yields system control) |

## B2 — Build/deploy (supply chain)

| STRIDE | Risk | Mitigation | DDS |
|--------|------|------------|-----|
| Spoofing | An attacker could impersonate a trusted software source in order to have malicious code accepted, leading to attacker-controlled code running in the system. | **Partial** — uv.lock pins and hash-verifies dependencies. *Open: no source/provenance policy beyond hashes.* | D2 |
| Tampering | An attacker could alter a dependency or build artifact in order to insert malicious code, leading to attacker-controlled code running in the system. | **Partial** — dependency hashes (uv.lock). *Open: base images pinned by tag not digest; no image signing/verification.* | D2 |
| Repudiation | An attacker could change what ships without leaving provenance in order to avoid attribution, leading to a malicious change that cannot be detected. | **Open** — no SBOM, build provenance, or commit/artifact signing. | D2 |
| Information disclosure | An attacker could extract secrets from the build process in order to obtain credentials, leading to exposure of user data. | **Partial** — `.dockerignore` excludes `.envs/` and `.git` from images; prod env files not in VCS. *Open: production secret-management strategy undecided; no build-time secret scanning.* | D1 |
| Denial of service | An attacker could disrupt the build or release pipeline in order to prevent shipping, leading to downtime and inability to recover. | **N/A yet** — no CI/CD pipeline configured; revisit when added. | D3 |
| Elevation of privilege | An attacker could abuse excessive pipeline permissions in order to introduce unauthorized code, leading to attacker-controlled code running in the system. | **N/A yet** — no CI/CD pipeline; define least-privilege when added. | D2 |

## Needs an attack tree next

Where a risk is really a tree of paths, decompose before rating (e.g. via MITRE ATT&CK):

- **B1 Spoofing + Elevation** — account takeover.
- **B2 Spoofing + Tampering** — supply-chain compromise.

## Open risks — mitigations still to develop

The outcome of this pass. Ordered roughly by priority.

1. **Access-control architecture** — object-level authorization, per-user query scoping, role model
   (B1 Tampering / Information disclosure / Elevation). *Biggest gap — drives D1.*
2. **MFA enforcement** decision (B1 Spoofing).
3. **Brute-force protection** beyond allauth defaults — API/token throttling, lockout (B1 Spoofing).
4. **Application-level rate limiting / DoS controls** (B1 Denial of service → D3).
5. **Security audit logging** of user/admin actions (B1 Repudiation).
6. **Supply-chain provenance** — SBOM + commit/artifact signing (B2 Repudiation).
7. **Base image digest pinning** + image verification (B2 Tampering).
8. **Dependency source/provenance policy** beyond hashes (B2 Spoofing).
9. **Production secret-management strategy** + build-time secret scanning (B2 Information disclosure).
10. **CI/CD security** — least-privilege pipeline, build availability — once a pipeline exists (B2 DoS / Elevation).
