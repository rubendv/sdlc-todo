# SDLC Policy

How secure development works on this project. Derived from the [SAMM assessment](samm-assessment.md):
it preserves the strong practices and sets minimum activities to raise the weak ones.

Scope: this repository. Owner: the operator (solo), who reviews all AI-assisted output.

## Principles

- Security work precedes feature code: threat model first, then requirements and tests, then build.
- Every decision traces to something — a doomsday scenario, a threat, a requirement, or a risk.
- Iterative: model and harden the highest risks first; record what is deferred as an accepted risk
  with a review trigger.
- Irreversible calls stay with a human: what gets installed, what ships, what is in scope.

## Required activities

**Design** (Threat Assessment / Security Requirements / Security Architecture)

- Threat-model new or changed features before building; update the threat-model docs and
  [backlog](../threat-model/README.md).
- Capture security requirements explicitly and trace each to a threat.
- Record architecture decisions and their security rationale.

**Implementation** (Secure Build)

- Dependencies pinned and hash-verified (`uv.lock`). No new third-party software without owner approval.
- No secrets in VCS beyond local dummy values; production secrets via the environment.
- Follow the [secure coding guidelines](../requirements/secure-coding-guidelines.md).

**Verification** (Requirements-driven Testing / Security Testing / Architecture Assessment)

- Security-relevant changes ship with positive **and** negative tests; update the
  [coverage matrix](../requirements/test-coverage.md).
- The security linter (ruff incl. bandit rules) must pass before commit. A proper SAST tool is not set
  up yet (RR-2).
- Re-review the threat model when the architecture or trust boundaries change.

**Governance** (Policy & Compliance / Defect Management)

- Commit in small steps with a message explaining why.
- New gaps go into the [risk register](../threat-model/risk-register.md) with a review trigger, not
  left implicit.

## Gates

- **Commit:** the security linter passes; tests pass; rationale in the message.
- **Feature-complete:** requirements traced and tested; coverage matrix current; new risks registered.
- **Before production deployment:** resolve all production-gated risks in the risk register, complete
  the threat-model backlog items that feed D1, stand up the Operations practices (incident response,
  backups, monitoring), and run the Django deployment checklist plus an ASVS pass.

## Maturity targets

From the assessment: every SAMM practice ≥ 1 before production; maintain ≥ 2 in Threat Assessment,
Security Requirements, and Requirements-driven Testing.

## Review

Reviewed when the SAMM assessment is redone (at least at each major milestone) or when a gate proves
inadequate.
