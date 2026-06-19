# Requirements

MVP requirements derived from the [threat model](../threat-model/README.md) so far, scoped to start
an initial implementation of the **core functionality**. We iterate per aspect later.

## Scope (this iteration)

- Core task tracking: accounts + CRUD on own tasks.
- The access-control and baseline security controls already established in the threat model.
- Runs **locally in a debug-enabled environment** — a good basis to build on, not production.

## Out of scope (this iteration)

- **Production settings / hardening** (TLS, HSTS, secure cookies, `DEBUG=False`, prod secrets) —
  not deploying anytime soon; local debug first.
- **Denial-of-service mitigations** (rate limiting, quotas) — D3 / STRIDE DoS.
- **Non-repudiation** (audit logging) — STRIDE Repudiation.
- Other deferred items tracked in [open risks](../threat-model/stride-analysis.md): MFA enforcement,
  supply-chain provenance (SBOM/signing/digest pinning), token lifecycle, account-deletion semantics.

## Index

- [functional-requirements.md](functional-requirements.md)
- [security-requirements.md](security-requirements.md)
- [secure-coding-guidelines.md](secure-coding-guidelines.md)
- [testing-strategy.md](testing-strategy.md)
- [test-coverage.md](test-coverage.md)

Sources: [doomsday-scenarios](../threat-model/doomsday-scenarios.md),
[stride-analysis](../threat-model/stride-analysis.md),
[access-control](../threat-model/access-control.md).
