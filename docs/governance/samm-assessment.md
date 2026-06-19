# OWASP SAMM Assessment

Basic self-assessment against [SAMM v2](https://owaspsamm.org), as of 2026-06-19. One maturity score
per practice (0–3): 0 none · 1 ad hoc/basic · 2 structured/repeatable · 3 measured/optimized. SAMM
scores two streams per practice; this is simplified to one score per practice for a first pass.

Context: early, solo, pre-production project. Design and Verification are intentionally ahead;
Operations and Deployment are near zero because there is no production yet.

## Governance

| Practice | Score | Basis |
|----------|:---:|-------|
| Strategy & Metrics | 0 | No security strategy, roadmap, or metrics. |
| Policy & Compliance | 1 | GDPR applicability identified; SDLC policy defined from this assessment. No compliance verification. |
| Education & Guidance | 1 | Secure coding guidelines documented; security-expert author. No formal training. |

## Design

| Practice | Score | Basis |
|----------|:---:|-------|
| Threat Assessment | 2 | Doomsday scenarios, iterative threat model, STRIDE, attack trees, risk register with triggers. Strongest area. |
| Security Requirements | 2 | Explicit security requirements traced to threats and to tests; third-party/scaffold risk partly considered. |
| Security Architecture | 1 | Access-control architecture and key decisions (no-CORS, defense-in-depth, fail-closed) documented. Not yet a reusable reference. |

## Implementation

| Practice | Score | Basis |
|----------|:---:|-------|
| Secure Build | 1 | Reproducible Docker build, hash-pinned dependencies (`uv.lock`), SAST (ruff/bandit) in pre-commit. No SBOM or signed artifacts (RR-9/10). |
| Secure Deployment | 0 | No deployment process or CI/CD; production deferred (RR-5). |
| Defect Management | 1 | Risks tracked in a register with triggers; no defect/vuln intake or metrics. |

## Verification

| Practice | Score | Basis |
|----------|:---:|-------|
| Architecture Assessment | 1 | Critical review of the threat model done; gaps backlogged. Not yet systematic per change. |
| Requirements-driven Testing | 2 | Positive + negative tests mapped to every in-scope requirement (coverage matrix). |
| Security Testing | 1 | SAST in pre-commit; SAST requirements + custom-rule plan defined. No DAST or pentest. ASVS not yet reviewed (RR-6). |

## Operations

| Practice | Score | Basis |
|----------|:---:|-------|
| Incident Management | 0 | No detection, logging, or response (threat-model backlog; RR-4). |
| Environment Management | 1 | Reproducible local Docker env; no patching/hardening process for prod (RR-5). |
| Operational Management | 0 | No data lifecycle, backup, or operational procedures (backlog). |

## Snapshot

- Strong: Design (Threat Assessment, Security Requirements) and Verification (Requirements-driven
  Testing) — the threat-led, requirements-traced, tested core.
- Weak: Operations (all three), Secure Deployment, Strategy & Metrics — expected pre-production.
- Lopsided by design: security thinking is well ahead of operational maturity.

## Targets

- **Before production:** every practice ≥ 1, and the production-gated risks resolved (see the
  [risk register](../threat-model/risk-register.md)). Raise the Operations practices from 0.
- **Maintain:** ≥ 2 in Threat Assessment, Security Requirements, and Requirements-driven Testing.

The [SDLC policy](sdlc-policy.md) turns these targets into required activities.
