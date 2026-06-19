# Risk-based security testing: let the threat model choose your CWEs

*Draft.*

Most security testing strategies I see start from a generic list: the OWASP Top 10, the CWE Top 25,
a scanner's default ruleset. They cover a lot, which sounds reassuring until you notice the coverage
has little to do with what would actually hurt the application in front of you. I gave a talk on
risk-based testing at SecAppDev 2026, and this is me working it through on a real codebase, the todo
app I'm building.

The approach is to let the threat model decide what you test and how.

## Start from the worst outcomes

The threat model already names three doomsday scenarios, ranked: disclosure of user data, the
infrastructure being used for lateral movement, and downtime that drives users away. That ranking is
the budget. Testing effort goes where the worst and most likely outcomes are, not where a checklist
spreads it evenly.

## Shortlist CWEs from attack trees

A generic CWE list covers what tends to go wrong across many systems. The question I care about is
narrower: what can go wrong in this one. To answer it I took the two most critical scenarios and built
small attack trees, asking how an attacker would reach that outcome through a coding mistake. Each leaf
is a concrete mistake, and each leaf gets a CWE.

For disclosure (D1) the leaves are mostly authorization: a missing object-level check (CWE-639,
CWE-862), a missing function-level permission (CWE-285, CWE-863), mass assignment of an owner or
privilege field (CWE-915). Then injection and over-exposure: SQL injection in raw queries (CWE-89),
broad serializers and verbose errors (CWE-200, CWE-209), stored XSS (CWE-79). For code execution (D2):
command injection (CWE-78), unsafe deserialization (CWE-502), SSRF (CWE-918).

That leaves about ten CWEs this app can plausibly suffer, ranked by how likely we are to introduce each
given the stack. It is a different list from the CWE Top 25, and it is the one worth writing tests and
rules for.

## Split the work by what each control is good at

With the shortlist in hand, assign each CWE to whatever verifies it best.

Authorization flaws are business logic. A scanner does not know that a task belongs to one user and not
another, so those are owned by tests, and specifically by negative tests: user A tries to read user B's
task and has to fail. Those tests are the core of the strategy.

Mechanical flaws are a better fit for static analysis. Command injection, unsafe deserialization,
raw-SQL patterns, `mark_safe` on user content: a static analyzer catches these well, and the scaffold
already runs Bandit's rules through Ruff, so some of it comes for free.

The authorization conventions sit in between. Off-the-shelf SAST will not understand them, but custom
rules will. A rule can require that every viewset overrides an owner-scoped `get_queryset`, that object
views set the ownership permission, that no serializer uses `fields = "__all__"`. Written for this app,
those rules enforce most of the authorization design structurally, which is the part I used to assume
only tests and review could cover.

What the custom rules still miss is deeper semantic correctness, such as a `get_queryset` that is
overridden but scoped to the wrong field. I would rather record that as an accepted risk and keep it
under manual review than pretend the coverage is complete.

## What you end up with

Every test and every rule traces back to a coding mistake, which traces to a critical risk, which
traces to a doomsday scenario. Nothing gets tested because a list said so. When someone asks why a
given test exists, the answer is a line you can follow all the way up.

The threat model and the testing strategy for this app live in [`docs/`](../). The talk this is based
on:
[Achieving risk-based and effective security testing (SecAppDev 2026)](https://secappdev.org/2026/sessions/achieving-risk-based-and-effective-security-testing/).
