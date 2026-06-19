# Governance for a project of one

*Draft.*

By this point the project had a threat model, security requirements, a test suite mapped to those
requirements, and a risk register. Good artifacts. But they existed because I happened to do the right
thing at each step, not because anything required them. That holds up until I forget, or until someone
else picks up the work and has no idea what the bar is. Governance is the part that turns a habit into
a rule.

So I ran a basic OWASP SAMM assessment and wrote a short SDLC policy from it. Both fit on a page. On a
solo, pre-production project that can sound like overkill, but the cost was about an hour and the
payoff was an honest picture of where the work actually stands.

## The assessment

SAMM v2 has fifteen security practices across five business functions: governance, design,
implementation, verification, and operations. I scored each from zero to three based on what the
project actually does, not on what I intend to do later.

The result was lopsided, which was the useful part. Threat assessment, security requirements, and
requirements-driven testing came out highest, because that is where the work has gone. Operations
scored zero across the board: no incident response, no monitoring, no backups. Secure deployment was
zero as well, because there is no deployment yet. Strategy and metrics was zero.

None of that is a surprise, and none of it is a failing for a project at this stage. The value is in
writing it down. "Operations is at zero" is a sharper statement than a vague sense that I will get to
operations eventually. It names the gap and puts it on the board.

## The policy

The assessment is a diagnosis. The SDLC policy is what I do about it. I derived the policy straight
from the scores: keep doing the things that scored well, and set a minimum bar for the things that did
not.

It is mostly a list of required activities, grouped the way SAMM groups them, plus three gates:

- At commit: static analysis passes, tests pass, and the message says why.
- At feature-complete: requirements are traced and tested, the coverage matrix is current, and any new
  gaps are in the risk register.
- Before production: every deferred risk with a "before production" trigger is resolved, the
  operations practices exist, and the app has been through the Django deployment checklist and an ASVS
  pass.

The before-production gate is where the deferred work comes due. All through the build I kept accepting
risks with the note "revisit before production." The policy is what makes that note enforceable rather
than aspirational. Nothing ships until that list is empty.

## Why bother on something this small

Governance has a reputation as the bureaucratic function, the one a small team skips. I think that is
backwards. The smaller the team, the more the process lives in one person's head, and the more it helps
to write the bar down so it survives a bad memory or a new contributor. The assessment took an hour and
told me the truth about the project. The policy fits on a page and turns a set of good habits into the
actual rules.

The assessment and policy are in the repo under docs/governance. Earlier posts cover the threat model,
the requirements and testing, and the implementation.
