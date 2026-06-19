# Turning the threat model into a tested API

*Draft.*

The earlier posts covered the planning: doomsday scenarios, a threat model, requirements, a CWE
shortlist, and a testing strategy. This one is about the code. I implemented the core of the todo
app, the task model and a locked-down API, and used the requirements as the checklist for what to
build and what to prove.

## Access control, two layers

The authorization design was already written down, so the implementation just followed it. Django
model permissions handle the function level: a user needs the right permission for the verb,
including view on reads, or the request is a 403 even when they own the object. A default group
grants those permissions, and new users join it at signup.

Ownership is the second layer. Each viewset scopes its queryset to the requesting user, and an
object-level permission checks ownership again as a backstop. The owner of a task is set on the
server from the authenticated user, never from the request body, and the serializer lists its fields
explicitly so a client cannot slip in an owner or a privilege flag.

Admins get no shortcut through the API. A superuser sees only their own objects there, the same as
anyone else; broader access will come through a separate channel.

## Tests as the proof

The testing strategy said the security tests lead and the negative cases carry the weight, so that is
how the suite is built. For each access-control requirement there is a test that the allowed action
works and a test that the forbidden one fails: a user cannot read another user's task, a missing
permission is a 403 even for the owner, a client-supplied owner is ignored, a superuser cannot reach
another user's records. One test checks the exact set of permissions a new user receives, so the
grant cannot quietly drift over time.

I kept a coverage matrix mapping every requirement to its positive and negative test. That turned
"are we done" into something I could read off the matrix instead of guess at. It also exposed the
holes: a few missing positive CRUD paths, and an admin-bypass check that existed for tasks but not
for users. I filled those.

## What I did not test, on purpose

Some things stayed out. Registration, email verification, and session login and logout are handled by
allauth, and I rely on its own tests rather than duplicating them. Instead of leaving that implicit, I
recorded it as an accepted risk with a trigger: if we customize those flows, we test them.

The same register holds the other deferrals: no denial-of-service controls, no audit logging, no
production hardening, and no pass against ASVS or the Django deployment checklist yet. Each has a
review trigger, and most share one, before any production deployment. Recording them as accepted
risks keeps a known gap from turning into a forgotten one.

## Steering, still

Even here the value was in the corrections, not the typing. The agent's first ownership check fell
back to comparing whatever object it was handed; I had it verify the owner is really a user, fail
closed otherwise, and log a warning when that happens. The self-delete handler logged the user out
unconditionally; I had it do so only when you delete yourself, so a future admin path will not log
the admin out. I dropped CORS entirely and will serve the frontend same-origin through the reverse
proxy, which removes a class of misconfiguration instead of configuring around it. And I asked for the
exact-permissions test by name, because "the user has the right permissions" is a weaker claim than
"the user has exactly these and no more."

None of that is the model being bad. It is what review is for.

The code, threat model, and requirements are in the repo. The earlier posts cover the planning and
the testing strategy.
