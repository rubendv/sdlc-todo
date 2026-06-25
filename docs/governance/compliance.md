# Compliance landscape

> **⚠️ NOT LEGAL ADVICE — NOT REVIEWED BY A LAWYER OR DPO.**
> This is a security engineer's best-effort map of *which rules likely apply and where the gaps are*,
> written to drive the work — **not** a compliance attestation. It has **not** been verified by a
> qualified legal or data-protection professional. Do not rely on it for a real launch. Before
> processing real personal data, have a competent privacy lawyer / DPO review everything here.

> **Example prompt:** *"Map the compliance landscape for this application. First ask me the scoping questions (real vs synthetic data, markets, who the controller is, where it's hosted). Then, from my answers, list the applicable regimes, inventory the personal data, map the key obligations to the current state, and list the gaps. Put a prominent disclaimer that this is not legal advice and not reviewed by a qualified professional."*

## Scope (from the scoping answers)

- **Real personal data** in production (not a synthetic-only demo) — obligations are live before launch.
- **Global users** — EU/EEA, UK, US, and potentially elsewhere.
- **Controller:** an individual operating this as a personal project. Note: offering it publicly to
  real users means the GDPR "purely personal or household activity" exemption **does not** apply — full
  controller obligations attach.
- **Hosting:** EU/EEA cloud.

## Applicable regimes (likely)

| Regime | Why it applies | Notes |
|--------|----------------|-------|
| **EU GDPR** | EU-based operator, EU users, EU hosting | Primary regime; drives most of this doc. |
| **UK GDPR + DPA 2018** | UK users | Largely mirrors EU GDPR. |
| **US state privacy laws** (CCPA/CPRA, VCDPA, CPA, …) | US users | Most have business-size/volume thresholds a small personal project likely *doesn't* meet — but verify; obligations (notice, rights) still good practice. |
| **ePrivacy (EU cookie rules)** | EU users | Only a strictly-necessary session cookie is used → consent banner likely not required. Re-check if any analytics/tracking is added. |
| Others (LGPD-Brazil, PIPEDA-Canada, …) | If genuinely global | Expand the list as real reach grows; out of scope for the first pass. |

## Personal data we process

| Data | Category | Notes |
|------|----------|-------|
| Email, username | Identity | Account + contact. |
| Password | Credential | Stored hashed (Argon2). |
| MFA secrets | Credential | If MFA used. |
| Session / API token | Authentication | Session in DB + Redis cache. |
| IP address / request logs | Identity (indirect) | Minimal logging today; grows with audit logging. |
| **Task content** (title, description) | **User-generated free text** | **May inadvertently contain special-category data (GDPR Art 9 — health, beliefs, etc.). Treat as sensitive.** |
| Timestamps | Activity | created/updated. |

## Roles & processors

- **Controller:** the operator (individual).
- **Processors** (need a data-processing agreement, and SCCs/Data Privacy Framework if outside the EEA):
  - **Hosting** — EU/EEA cloud (no third-country transfer for hosting itself).
  - **Email/SMTP provider** — verify its location; if US-based, an international transfer applies.
  - Any future analytics, error-tracking (Sentry), or CDN — each is a processor/transfer to assess.

## Key obligations vs current state

`✅` reasonable · `⚠️` partial · `❌` gap. Most map onto existing security work or the risk register.

| Obligation | State | Notes / link |
|------------|-------|--------------|
| Lawful basis (Art 6) | ❌ | Define per purpose (contract for the account; legitimate interest for security logs). |
| Transparency / privacy notice (Art 13–14) | ❌ | No privacy policy yet. |
| Security of processing (Art 32) | ⚠️ | Driven by the threat model + controls; production hardening deferred (RR-5). |
| Right of access & portability (Art 15, 20) | ❌ | No "export my data" capability yet. |
| Right to erasure (Art 17) | ⚠️ | Account self-delete (FR-3) cascades to tasks; **does not** yet cover logs, backups, or cached sessions. |
| Right to rectification (Art 16) | ✅ | Users can update their account and tasks via the API. |
| Restriction / objection (Art 18, 21) | ❌ | Not implemented. |
| Breach notification — 72h (Art 33–34) + US state laws | ❌ | **Cannot detect or scope a breach** — no audit logging/monitoring (RR-4, detection backlog). Major gap. |
| DPIA (Art 35) | ❌ | Free-text fields + possible special-category data + global scale → likely advisable; assess. |
| Records of processing (Art 30) | ❌ | Small-scale individuals can be exempt, but processing that may include special-category data removes the exemption → needed. |
| Data minimization & retention (Art 5) | ❌ | No retention policy; define how long accounts/tasks/logs are kept. |
| Age / children (Art 8; US COPPA) | ❌ | Public sign-up → set a minimum age and handle consent, or restrict. |
| International transfers (Ch. V) | ⚠️ | EU hosting is fine; check each non-EEA processor (email, etc.) for SCCs/DPF. |
| US notice & rights (CCPA/CPRA) | ⚠️ | "Notice at collection" + consumer rights; no "sale/share" of data here. Thresholds likely unmet — verify. |

## Gaps to close before processing real data

1. Privacy notice + documented lawful bases.
2. Data-processing agreements with all processors; SCCs/DPF for any non-EEA transfer.
3. Data-subject-rights tooling: export (access/portability), full erasure (incl. logs, backups, cache).
4. **Breach detection + response process** — depends on audit logging/monitoring (RR-4, threat-model
   detection backlog).
5. Retention policy + automated enforcement.
6. DPIA decision (and the DPIA if indicated).
7. Records of processing (Art 30).
8. Age gating / children's-data handling.
9. **A review by a qualified privacy professional** (see the disclaimer).

## Relationship to the rest of the SDLC

- *Security of processing* (Art 32) leans on the [threat model](../threat-model/README.md) and
  [risk register](../threat-model/risk-register.md).
- *Breach notification* depends on the **Detection & response** threat-model backlog item and RR-4.
- *Erasure / retention* tie to FR-3 and the **Data lifecycle & privacy** backlog item.
- All of the above are gated **before production** alongside the other deferred risks.

## Status

Not started as actual compliance work — this is a landscape map to scope it. None of it is verified by
a legal expert.
