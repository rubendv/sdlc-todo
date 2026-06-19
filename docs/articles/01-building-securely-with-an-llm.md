# Building a secure app with an LLM while keeping oversight

*Draft.*

I run security programs for clients. The advice rarely changes: move security earlier in the SDLC so
the process turns out secure software without heroics at the end. To make that concrete I'm building
a small todo API as an example, one step at a time.

I built it together with an LLM agent (Claude Code). The aim was to go faster without handing over
the decisions. Here is how the collaboration worked, and where I had to correct it.

## Ground rules

I set a few constraints before starting.

The agent had to ask before installing anything. When it needed Docker with buildx and cookiecutter,
it stopped and gave me the commands to run myself.

It had to surface decisions rather than assume them.

Every step became its own commit, with a message that records why the change was made. The history
is enough to rebuild the project from scratch, including the notes behind this article.

## Security work before code

No application logic got written until the security design was in place. The order was:

1. Doomsday scenarios. Three worst-case outcomes, ranked: disclosure of user data; the
   infrastructure being used for lateral movement or malware; and downtime bad enough that people
   stop using the app. Every later risk maps back to one of these.
2. Context diagram and a level-1 data-flow diagram. Break the monolith into its parts, mark the
   trust boundaries, and rank them so the perimeter gets the attention.
3. STRIDE on the perimeter boundaries. Each risk written in plain language and tied to a doomsday
   scenario, with a column showing what the scaffold already handles and what is still open.
4. Access-control design. Django model permissions checked at the function level, then narrowed to
   the owner of each object.
5. Requirements and a testing strategy, scoped to an MVP, with each security requirement linked back
   to a threat.

Implementation starts from that written target.

## Corrections I made

The agent is quick and usually competent. It is also wrong often enough that running it unsupervised
would be a mistake, so most of my time went into steering it. Some examples from this build:

- It defaulted to the newest Django when I had asked for an LTS release. I later reversed that
  decision myself. Either way the version was chosen on purpose instead of inherited from a template.
- Its writing ran long and over-decorated. I asked for terse and technical and made that a standing
  rule, and it stopped padding.
- It got ahead of itself. During the doomsday-scenario step it began listing attack vectors, which
  belongs to a later stage. I held each step to its own scope.
- It modeled admin access in a way I did not want. Admins get no shortcut through the API; there they
  see only their own objects, the same as anyone else, and broader access comes through a separate
  channel. I rewrote that and it followed.
- I took production out of scope for now. I want a working local setup with debug enabled before any
  hardening.

None of this is unusual. It is the ordinary work of reading what the tool produces and redirecting
it. The speed-up was real, and it depended on that review.

## What I took from it

The agent earns its keep when a clear process already exists for it to follow. It will not supply
that process. The way I get value from it is to ask for its reasoning and to make every decision
point at something concrete, like a threat or a requirement, because the decisions with no stated
basis are the ones that need the closest look. The calls I keep for myself are the ones that are hard
to undo: what gets installed, what gets shipped, what stays in scope. And I commit in small pieces
with the reason written down, since I reread those messages more than I expected to.

The threat model and requirements behind the app live in [`docs/`](../). Next is the first real
implementation: the task model and a locked-down API.
