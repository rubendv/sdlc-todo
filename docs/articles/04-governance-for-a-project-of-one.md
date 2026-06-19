# Governance for a project of one

*Draft.*

By this point the project had a threat model, security requirements, a test suite mapped to those
requirements, and a register of known risks. Good artifacts. But they existed because I happened to do
the right thing at each step, not because anything required them. That holds up until I forget, or
until someone else picks up the work and has no idea what the bar is. Governance is the unglamorous
part that turns a habit into a rule.

So I ran a basic OWASP SAMM assessment and wrote a short SDLC policy from it. SAMM (the Software
Assurance Maturity Model) is a structured way to score how mature your security practices are; an SDLC
policy is a short statement of how you build software and what each step must include. Both fit on a
page. On a solo, pre-production project that can sound like overkill, but it cost about an hour and the
payoff was an honest picture of where the work actually stands.

## The assessment

SAMM lists fifteen security practices across five areas: governance, design, implementation,
verification, and operations. I scored each from zero to three based on what the project actually does,
not on what I intend to do later.

The result was lopsided, which was the useful part. The design and verification practices — threat
modeling, security requirements, requirements-driven testing — came out highest, because that is where
the work has gone. Operations scored zero across the board: no incident response, no monitoring, no
backups. Deployment was zero, because there is no deployment yet. So was overall security strategy. And
I still have not rated my risks by likelihood and impact, which the assessment dutifully surfaced too.

None of that is a surprise, and none of it is a failing at this stage. The value is in writing it down.
"Operations is at zero" is a sharper statement than a vague sense that I will get to operations
eventually. It names the gap and puts it on the board.

## The policy

The assessment is a diagnosis. The SDLC policy is what I do about it. I derived the policy straight from
the scores: keep doing the things that scored well, and set a minimum bar for the things that did not.

It is mostly a list of required activities, grouped the way SAMM groups them, plus three gates — points
where work is not allowed to proceed until certain things are true:

- At commit: the security linter passes, the tests pass, and the message says why the change was made.
- At feature-complete: requirements are traced and tested, the coverage table is current, and any new
  gaps are written into the risk register.
- Before production: every risk marked "revisit before production" is resolved, the operations
  practices exist, and the app has been through the standard deployment and security-verification
  checklists (the Django deployment checklist and OWASP ASVS, a catalog of security requirements to
  check an app against).

The before-production gate is where the deferred work comes due. All through the build I kept accepting
risks with the note "revisit before production." The policy is what makes that note enforceable rather
than aspirational. Nothing ships until that list is empty.

## Why bother on something this small

Governance has a reputation as the bureaucratic function, the one a small team skips. I think that is
backwards. The smaller the team, the more the process lives in one person's head, and the more it helps
to write the bar down so it survives a bad memory or a new contributor. None of this was done all at
once, either: the assessment and policy came after the threat model and the code, as one more step in
an incremental process. It took an hour, told me the truth about the project, and fits on a page.

The assessment and policy are in the repo. Earlier posts cover the threat model, the requirements and
testing, and the implementation.
