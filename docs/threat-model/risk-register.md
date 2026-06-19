# Risk Register

The project's risks and their treatment: consciously accepted residual risks, and open risks with a
planned mitigation. Each has a rationale and a trigger that says when to revisit it. Most deferrals
share one trigger: **before any production deployment**.

**Risks are not yet rated.** Likelihood, impact, and a resulting priority are still to do (see the
threat-model [backlog](README.md#not-yet-modeled-backlog)). For now ordering is rough and by hand, and
each risk links to the doomsday scenario it would cause.

| ID | Risk | Decision | Rationale | Review trigger |
|----|------|----------|-----------|----------------|
| RR-1 | A defect or misconfiguration in the allauth auth flows (registration, email verification, login/logout) could enable account takeover or unauthorized access and go unnoticed, because we rely on upstream tests rather than our own (FR-1, SR-3, part of FR-2 → D1). | Accept | Provided and tested upstream by django-allauth; our scope is the custom API and access control. The API's acceptance of session and token auth *is* tested. | We customize the signup, verification, or login flow. |
| RR-2 | An authorization bug that custom SAST rules cannot detect (e.g. a `get_queryset` scoped to the wrong field) could reach production and expose one user's data to another (→ D1). | Accept | Custom rules cover the structural conventions; the residual is caught by negative access-control tests and review. | The custom rules mature, or an authz bug slips through. |
| RR-3 | With no rate limiting, quotas, or throttling, an attacker or runaway client could exhaust resources and make the service unavailable (STRIDE DoS → D3). | Accept (this iteration) | Local, debug-only basis; not publicly exposed. | Before any production / public deployment. |
| RR-4 | With no audit log of user/admin actions, a breach could occur without being detected or reconstructed, delaying response and preventing accurate scoping (STRIDE Repudiation → amplifies D1/D2). | Accept (this iteration) | Out of MVP scope; not needed for a local basis. | Before production deployment, or if compliance requires it. |
| RR-5 | Deployed without hardening (no TLS/HSTS, `DEBUG` on, weak secret handling), the app could expose data in transit or leak internal detail and credentials (SR-4, SR-11 → D1). | Accept (local-only) | Running locally in debug by design; currently avoided only by not deploying. | Before any non-local / production deployment. |
| RR-6 | Without an ASVS v5 / Django deployment-checklist review, required security controls could be missing unnoticed, leaving unknown exposure (→ D1/D2). | Accept (this iteration) | Threat-model-driven controls came first; a standards pass is later work. | Before production deployment. |
| RR-7 | With MFA available but not enforced, a single stolen, phished, or guessed password is enough to take over an account (B1 Spoofing → D1). | Open — mitigate | Enforcement is an auth-hardening decision deferred past the MVP core. | Before production, or when signup opens to untrusted users. |
| RR-8 | Without throttling or lockout on the API and token endpoints, an attacker could brute-force or credential-stuff at scale and take over accounts (B1 Spoofing → D1). | Open — mitigate | Default allauth limits cover the login view; the API/token paths are unthrottled. | Before production / public exposure. |
| RR-9 | Without build provenance (SBOM, commit/artifact signing), a tampered dependency or artifact could be introduced and run undetected, leading to code execution or data theft (B2 Repudiation → D2). | Open — mitigate | Dependencies are hash-pinned via `uv.lock`; provenance and signing are not in place. | Before production, or when a release pipeline exists. |
| RR-10 | Because base images are pinned by mutable tag rather than digest, a changed or poisoned upstream image could be pulled into a build and run attacker-controlled code (B2 Tampering → D2). | Open — mitigate | Tag pinning is mutable; no image verification. | Before production. |
| RR-11 | Without a dependency source policy beyond integrity hashes, a malicious or typosquatted package could be added and trusted, compromising the build (B2 Spoofing → D2). | Open — mitigate | `uv.lock` verifies integrity but there is no source allowlist or policy. | Before production. |
| RR-12 | Without a least-privilege CI/CD pipeline, leaked pipeline credentials or an over-privileged job could push malicious code to production (B2 Elevation / DoS → D2). | Open — mitigate | No CI/CD pipeline exists yet. | When a CI/CD pipeline is introduced. |

Each risk is revisited at its trigger; none is permanent.
