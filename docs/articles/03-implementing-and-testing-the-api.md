# Turning the threat model into a tested API

*Draft.*

The earlier posts covered the planning: the worst-case outcomes, the threat model, the requirements,
and the testing strategy. This one is about the code. I built the core of the todo app — the tasks and
accounts behind a web API — and used the requirements as the checklist for what to build and what to
prove.

## Access control, in two layers

Access control means deciding who is allowed to do what. The design was already written down, so the
code just followed it, and it works in two independent layers so that a single slip does not open
everything.

The first layer is permissions: every user is granted a specific set of allowed actions (view, create,
change, delete), and the API refuses anything not on that list, even reading, and even when the user
owns the thing they are asking for. The second layer is ownership: every database query is limited to
the current user's own rows, and a separate check confirms ownership before any single record is
touched. A task's owner is set by the server from whoever is logged in, never taken from the incoming
request, and the API accepts only the handful of fields it should, so a client cannot sneak in a
different owner or an "is admin" flag.

Admins get no shortcut through the API. An admin account sees only its own data there, like anyone
else; broader access, if we add it, will come through a separate channel, not by making the API trust
the request more.

## Tests as the proof

The testing strategy said the security tests lead and the "this must fail" cases carry the weight, so
that is how the suite is built. For each access-control rule there is a test that the allowed action
works and a test that the forbidden one is refused: a user cannot read another user's task, a user
missing the right permission is refused even on their own task, a client-supplied owner is ignored, an
admin cannot reach another user's records. One test pins down the exact set of permissions a new user
gets, so that set cannot quietly grow over time.

I kept a coverage matrix — a simple table mapping every requirement to its "works" and "is refused"
tests. That turned "are we done?" into something I could read off the table instead of guess at. It
also exposed holes: a couple of missing checks on the normal happy path, and an admin check I had
written for tasks but not for accounts. I filled them.

## What I have not tested yet

Some things stayed out of this pass. Sign-up, email verification, and logging in and out are handled by
a well-known library (django-allauth). For now I lean on its upstream tests rather than writing my own.
But these flows are the front door to every account, the most likely way someone takes one over, so I
will test them myself before this goes anywhere near production. They are deferred, not skipped: it is
written down as an accepted risk whose trigger says exactly that, test before production (and sooner if
we customize those flows).

The same risk register holds the other deferrals: no protection against traffic floods, no audit log,
no production hardening yet. Each is written as an actual risk — what could happen and why it matters,
not just "todo: add X" — with a trigger that says when to come back to it, usually before going to
production. I have not rated them by likelihood and impact yet; that is itself on the list. Writing a
gap down this way keeps it from quietly becoming a forgotten one.

## Steering, still

Even here, the value was in the corrections, not the typing. The agent's first ownership check would
compare against whatever object it was handed; I had it confirm the object actually has a real user as
its owner, refuse by default when unsure, and log a warning if that ever happens. Its account-deletion
code logged the user out every time; I had it do so only when you delete your own account, so a future
"admin deletes a user" path will not boot the admin out of their own session. I dropped CORS — the
browser mechanism for letting one website call another's API — and will instead serve the frontend from
the same address as the API, which removes a whole class of misconfiguration rather than carefully
configuring around it. And I asked for the exact-permissions test by name, because "the user has the
right permissions" is a weaker claim than "the user has exactly these and no more."

None of that is the model being bad. It is what review is for.

This is a fast first pass and not yet thoroughly reviewed; the code and the threat model are in the
repo for reading, not as a finished reference. The earlier posts cover the planning and the testing
strategy.
