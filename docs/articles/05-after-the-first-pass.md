# After the first pass: prompts as artifacts, a validation round, and compliance

*Outline. The points that need to be made here, to be written up in my own voice later.*

## What this article is for

- The first four posts walked through building the app: the threat model, the requirements and tests,
  the implementation, and the governance layer.
- Since then I have added almost no new functionality. The work has been about the example itself —
  making it reproducible, making it readable, checking it holds together, and extending it into
  compliance. This post is about those evolutions.

## The prompt that made each document goes in the document

- Every artifact in this repo was produced by prompting an LLM. So I started putting the prompt that
  generates each document at the top of that document.
- Each one names the inputs it should read (the earlier artifacts), the shape of the output, and a
  standing instruction: ask me about anything that is a product or risk decision, and do not assume it.
- That last part matters. The threat model only works if the doomsday scenarios and the risk decisions
  are mine. A prompt that says "ask me, do not guess" stops the model from quietly inventing the context
  that the whole analysis hangs on.
- Putting the prompt in the document does two things:
  - It makes the work reproducible: someone can read the prompt, point it at the same inputs, and
    regenerate a comparable artifact.
  - It makes the process teachable, which is the point of the repo, by showing the exact question that
    produced each result.

## Checking the documents against their own prompts

- Once each document carried its prompt, I could run the prompt in my head against the document and ask
  whether the output actually matches what the prompt asked for. I went through all of them this way.
- It caught real problems:
  - The data-flow diagram numbered its data stores D1 and D2, which collided with the doomsday
    scenarios D1 and D2 — I renamed the stores.
  - The risk register's prompt asked for a particular phrasing the entries did not follow, so I
    rewrote the entries (and adjusted the prompt for the risks that are process gaps rather than
    attacker actions).
  - The functional requirements never said what was out of scope, though the prompt asked for it.
  - None of these were dramatic, but they are the kind of drift that makes a document slowly stop
    meaning what it claims.
- A couple of the mismatches were design decisions in disguise. The context diagram only listed people
  as external entities, but the prompt asked for external systems too. The rule we landed on: a system
  is an "external entity" only if we are not going to threat-model it properly; the mail server and the
  package registry, which we do want to analyze, are better drawn as processes outside our trust
  boundary. The validation did more than fix wording; it sharpened the model.

## One new concern, threaded through everything

- The newest addition is compliance. I wrote a document mapping which privacy laws would apply if this
  ran for real — GDPR, the UK equivalent, US state laws — what personal data we hold, and where the
  gaps are. It opens with a loud disclaimer: I am not a lawyer, none of it is legal advice, and a real
  launch needs a professional to review it.
- What struck me was how far that one document reached. Adding compliance meant:
  - a new entry in the risk register (unaddressed compliance, with fines and legal action as the
    impact),
  - a bump in the governance assessment,
  - and a few cheap requirements I could add right away — letting a user export their data, confirming
    that deleting an account removes their tasks, and keeping to a single strictly-necessary cookie.
- One concern, and it touched the risk register, the maturity assessment, the requirements, and the
  story itself. That is the sign the artifacts are genuinely connected, not just filed in the same
  folder.

## Reading it back

- The other thread has been plain editing. The first drafts, including these posts, were written by
  the model and read like it. I have been going through them in my own voice, and making the whole
  thing approachable for developers without a security background: a glossary, fewer acronyms, and a
  README that explains the idea before the jargon.
- The repo is meant to be a worked example someone can learn from, and that only works if they can
  read it.
- None of this is new functionality. It is the unglamorous side of a worked example: keeping it honest
  and readable, and keeping the pieces in sync as it grows.
