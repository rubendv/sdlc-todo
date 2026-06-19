# Building a secure app with an LLM while keeping oversight

*Draft.*

I run security programs for clients. The advice rarely changes: build security into the process of
making software (the software development life cycle, or SDLC) from the start, so good security falls
out the end instead of being bolted on in a panic. To make that concrete I am building a small todo API
as an example, one step at a time, and writing up each step for developers who have never watched this
done up close.

I built it together with an LLM coding agent (Claude Code). The aim was to go faster without handing
over the decisions. Here is how the collaboration worked, and where I had to correct it.

## Ground rules

I set a few constraints before starting.

The agent had to ask before installing anything. When it needed Docker and a project generator, it
stopped and gave me the commands to run myself.

It had to surface decisions rather than assume them.

Every step became its own commit, with a message that records why the change was made. The history is
enough to rebuild the project from scratch, including the notes behind this article.

## Security work before code

No application logic got written until the security design was in place. The order, roughly:

1. Worst-case outcomes. I named the three things that would genuinely hurt if they happened: user data
   leaking, the server being hijacked to attack others, and downtime bad enough that users leave.
   Everything later is judged against these. (In the docs I call them doomsday scenarios.)
2. A map of the system. Simple diagrams of how data moves, marking where it crosses from a
   less-trusted zone into a more-trusted one — the trust boundaries, where most risk lives, so they get
   the attention first.
3. A threat pass. Walking those boundaries against a standard checklist of threat types (called STRIDE)
   so I do not forget a category, and tying each threat back to one of the worst-case outcomes.
4. Access control. Deciding who can do what: users can reach only their own data, enforced in two
   independent ways so a single mistake does not open everything.
5. Requirements and a testing plan, kept deliberately small, each security requirement linked back to a
   specific threat.

Only then does the code start, written against that target. The work is iterative, not one grand plan:
I model the highest risks first and keep a backlog of what I have not modeled yet, so the gaps stay
visible instead of forgotten.

## Corrections I made

The agent is quick and usually competent. It is also wrong often enough that running it unsupervised
would be a mistake, so most of my time went into steering it. Some examples from this build:

- It defaulted to the newest version of the web framework when I had asked for a long-term-support
  release (the boring one that stays patched for years). I later changed my own mind and went back to
  the newest. Either way the choice was deliberate, not inherited from a template.
- Its writing ran long and over-decorated. I asked for terse and technical and made that a standing
  rule, and it stopped padding.
- It got ahead of itself. During the worst-case-outcomes step it started listing specific attack
  methods, which belongs to a later stage. I held each step to its own job.
- It modeled admin access in a way I did not want. Through the API, admins get no shortcut; they see
  only their own data, like anyone else, and broader access will come through a separate channel. I
  rewrote that and it followed.
- I took production out of scope for now. I want a working setup on my own machine before any
  production hardening.

None of this is unusual. It is the ordinary work of reading what the tool produces and redirecting it.
The speed-up was real, and it depended on that review.

## What I took from it

The agent earns its keep when a clear process already exists for it to follow. It will not supply that
process. The way I get value from it is to ask for its reasoning and to make every decision point at
something concrete, like a threat or a requirement, because the decisions with no stated basis are the
ones that need the closest look. The calls I keep for myself are the ones that are hard to undo: what
gets installed, what gets shipped, what stays in scope. And I commit in small pieces with the reason
written down, since I reread those messages more than I expected to.

In fairness, this is a fast first pass, built in about a day and not yet thoroughly reviewed. The point
is the approach, not a finished product. The threat model and requirements live in the repo. Next is
the first real implementation: the data model and a locked-down API.
