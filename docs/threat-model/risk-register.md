# Risk Register

The project's risks and their treatment: consciously accepted residual risks, and open risks with a
planned mitigation. Each has a rationale and a trigger that says when to revisit it. Most deferrals
share one trigger: **before any production deployment**.

| ID | Risk | Decision | Rationale | Review trigger |
|----|------|----------|-----------|----------------|
| RR-1 | allauth-owned auth flows — registration, mandatory email verification, session login/logout (FR-1, SR-3, part of FR-2) — are not covered by our own automated tests. | Accept | Provided and tested upstream by django-allauth; our scope is the custom API and access control. The API's acceptance of session and token auth *is* tested. | We customize the signup, verification, or login flow. |
| RR-2 | SAST cannot verify deeper authorization semantics (e.g. a `get_queryset` scoped to the wrong field) — only the structural conventions. | Accept | Custom rules cover the conventions; the residual is caught by negative access-control tests and review. | The custom rules mature, or an authz bug slips through. |
| RR-3 | No denial-of-service mitigations: no rate limiting, quotas, or throttling (D3, STRIDE DoS). | Accept (this iteration) | Local, debug-only basis; not publicly exposed. | Before any production / public deployment. |
| RR-4 | No non-repudiation: no security audit log of user/admin actions (STRIDE Repudiation). | Accept (this iteration) | Out of MVP scope; not needed for a local basis. | Before production deployment, or if compliance requires it. |
| RR-5 | Production settings and hardening not configured or reviewed: TLS, HSTS, secure cookies, `DEBUG=False`, production secret management (SR-4, SR-11). | Accept (local-only) | Running locally in debug by design. | Before any non-local / production deployment. |
| RR-6 | ASVS v5 and the Django deployment checklist have not been reviewed against this app. | Accept (this iteration) | Threat-model-driven controls came first; a standards pass is later work. | Before production deployment. |
| RR-7 | MFA is available (allauth) but not enforced (B1 Spoofing → D1). | Open — mitigate | Enforcement is an auth-hardening decision deferred past the MVP core. | Before production, or when signup opens to untrusted users. |
| RR-8 | No brute-force protection beyond allauth's default login rate limits — API/token throttling and lockout (B1 Spoofing → D1). | Open — mitigate | Default allauth limits cover the login view; the API/token paths are unthrottled. | Before production / public exposure. |
| RR-9 | No supply-chain provenance: no SBOM, commit or artifact signing (B2 Repudiation → D2). | Open — mitigate | Dependencies are hash-pinned via `uv.lock`; provenance and signing are not in place. | Before production, or when a release pipeline exists. |
| RR-10 | Base images are pinned by tag, not digest; no image verification (B2 Tampering → D2). | Open — mitigate | Tag pinning is mutable. | Before production. |
| RR-11 | No dependency source/provenance policy beyond integrity hashes (B2 Spoofing → D2). | Open — mitigate | `uv.lock` verifies integrity but there is no source allowlist or policy. | Before production. |
| RR-12 | No CI/CD security: least-privilege pipeline, build availability (B2 DoS / Elevation). | Open — mitigate | No CI/CD pipeline exists yet. | When a CI/CD pipeline is introduced. |

Each risk is revisited at its trigger; none is permanent.
