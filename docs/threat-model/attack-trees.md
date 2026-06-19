# Attack Trees — critical risks

Decompose the two most critical [doomsday scenarios](doomsday-scenarios.md) into the **coding
mistakes** that enable them, so we can shortlist the CWEs that matter for *our* code. Leaves are tagged
with a CWE. Build-time and infra paths are out of scope here (covered by SR-13–15); this is about
mistakes a developer makes in the application.

Trees are OR unless noted. Framework defaults already block some leaves (ORM, template escaping,
CSRF) — they stay in the tree because we can still break them.

## D1 — read data the caller shouldn't

- Become another principal (authentication)
  - Custom/broken auth or login logic — CWE-287
  - Session fixation, or long-lived tokens never revoked — CWE-384, CWE-613
  - Credentials handled insecurely (logged, in URLs) — CWE-522
- Act as a valid user but reach others' data (authorization) ← *most likely for us*
  - Missing object-level check / IDOR (queryset not scoped to owner) — CWE-639, CWE-862
  - Missing or wrong function-level permission — CWE-863, CWE-285
  - Mass assignment of `owner` / privilege fields — CWE-915
- Extract via injection
  - SQL injection through raw queries / string-built SQL — CWE-89
- Over-expose data
  - Serializer returns extra fields or others' records — CWE-200
  - Verbose errors / debug detail in responses — CWE-209
- Steal client-side (frontend)
  - Stored XSS in task content, used to lift a session/token — CWE-79

## D2 — run code or pivot to other systems

- Code execution in the app
  - OS command injection (shelling out with user input) — CWE-78
  - Deserialization of untrusted data (pickle, `yaml.load`) — CWE-502
- Reach internal systems
  - SSRF from a user-supplied URL the server fetches — CWE-918
- Untrusted file handling
  - Path traversal / unrestricted upload — CWE-22, CWE-434

## CWE shortlist

Prioritized for this codebase (Django/DRF, MVP). Tier 1 is where we are most likely to introduce the
flaw ourselves; it maps straight to the [access-control](access-control.md) work.

| # | CWE | Mistake | Risk |
|---|-----|---------|------|
| 1 | CWE-639 / CWE-862 | Broken/missing object-level authorization (IDOR/BOLA) | D1 |
| 2 | CWE-285 / CWE-863 | Improper/incorrect function-level authorization | D1 |
| 3 | CWE-915 | Mass assignment of protected fields | D1 |
| 4 | CWE-200 / CWE-209 | Sensitive-data / error over-exposure | D1 |
| 5 | CWE-89 | SQL injection via raw queries | D1 |
| 6 | CWE-79 | Stored XSS in user content | D1 |
| 7 | CWE-502 | Insecure deserialization | D2 |
| 8 | CWE-78 | OS command injection | D2 |
| 9 | CWE-918 | SSRF | D2 |
| 10 | CWE-287 / CWE-384 / CWE-613 | Broken authentication / session handling | D1 |

CWE-22 / CWE-434 (file handling) are parked — no uploads in the MVP; revisit if that changes.

These feed the [secure coding guidelines](../requirements/secure-coding-guidelines.md).
