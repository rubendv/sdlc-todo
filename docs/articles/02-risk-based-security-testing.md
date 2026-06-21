# Risk-based security testing: let the threat model choose what to test

*LLM Draft. Placeholder until I rewrite in my own voice*

Most security testing plans I see start from a generic list: the OWASP Top 10, the CWE Top 25, a
scanner's default rules. (A CWE, Common Weakness Enumeration, is just a numbered catalog of types of
software weakness, like "SQL injection" or "missing authorization.") Those lists cover a lot, which
sounds reassuring until you notice the coverage has little to do with what would actually hurt the app
in front of you. I gave a talk on risk-based testing at SecAppDev 2026, and this is me working it
through on a real codebase, the todo app I am building.

The approach is to let the threat model — the up-front analysis of what could go wrong — decide what
you test and how.

## Start from the worst outcomes

The threat model names three worst-case outcomes, ranked: user data leaking, the infrastructure being
used to attack others, and downtime that drives users away. That ranking is the budget. Testing effort
goes where the worst and most likely outcomes are, not spread evenly because a checklist said so.

## Work out the specific mistakes that lead there

A generic weakness list tells you what tends to go wrong across many systems. The question I care about
is narrower: what can go wrong in this one. So I took the two most serious outcomes and drew small
attack trees — diagrams that start from a bad outcome and branch downward into the steps an attacker
would take to reach it. Each branch ends at a concrete coding mistake, and I label that mistake with
its CWE so there is no ambiguity about which one I mean.

For data disclosure, most branches are about authorization (controlling who can access what): one user
reaching another user's records, an endpoint that forgets to check permission at all, or a request that
quietly sets a field it should not, like the record's owner. The rest are injection and over-sharing:
SQL injection, responses that return more than intended, and stored cross-site scripting (malicious
text saved by one user and run in another user's browser). For the server-takeover outcome: command
injection, unsafe handling of incoming data, and SSRF, where the server is tricked into making requests
on an attacker's behalf.

That leaves about ten weaknesses this app could plausibly have, ranked by how likely we are to
introduce each one given our tools. It is a far shorter and more relevant list than the CWE Top 25, and
it is the one worth writing tests and rules for.

## Split the work by what each tool is good at

With the shortlist in hand, give each weakness to whatever checks it best.

Authorization flaws are business logic. A scanner has no idea that a given task belongs to one user and
not another, so these are owned by tests, and specifically by negative tests — checks that a forbidden
action actually fails. User A tries to read user B's task and must be refused. Those tests are the core
of the strategy.

Mechanical flaws are a better fit for static analysis, often shortened to SAST: tools that read your
source code and flag risky patterns without running it. Command injection, unsafe data handling, raw
SQL, marking attacker-controlled text as safe to display — a static analyzer catches these well. The
project runs a basic security linter today, which picks up a few of them for free, but that is not a
real SAST tool, and setting one up is still on the to-do list.

The authorization conventions sit in between. Off-the-shelf scanners do not understand them, but custom
rules can. I can write a rule that requires every endpoint to limit its database query to the current
user's own rows, and that forbids the shortcuts which would expose everything. Written for this app,
such rules would enforce most of the authorization design automatically — the part I used to assume
only tests and review could cover. That is the plan; it is not built yet.

What the custom rules still miss is deeper correctness, like a query limited to the wrong field. I
would rather record that as a known, accepted risk and keep it under manual review than pretend the
coverage is complete. One thing I have not done yet is actually rate these risks by how likely and how
damaging each is; that is on the list too.

## What you end up with

Every test and every rule traces back to a coding mistake, which traces to a serious outcome, which
traces to one of the three worst cases. Nothing gets tested because a list said so. When someone asks
why a given test exists, the answer is a line you can follow all the way up.

The threat model and the testing strategy live in the repo. The talk this is based on:
[Achieving risk-based and effective security testing (SecAppDev 2026)](https://secappdev.org/2026/sessions/achieving-risk-based-and-effective-security-testing/).
