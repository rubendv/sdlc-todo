# Doomsday Scenarios

> **Example prompt:** *"Identify this application's doomsday scenarios. Input: my answers to your questions — there is no prior artifact yet. First ask me about the business context: what the product does, who its users are, what data it holds, and what outcomes would be catastrophic for the users and the business. Do not assume any of this. Output: the three worst outcomes, ranked, each a short heading plus a one-line impact statement, in Markdown."*

Three catastrophic outcomes, every security activity is aimed at preventing these scenarios from happening or reducing their impact if they do happen.

## D1 — Disclosure of user data

Someone reads data they shouldn't: task content, or identity data (emails, password hashes, MFA
secrets) — one user or the whole base. Irreversible once out. GDPR-reportable.

## D2 — Infra used for lateral movement or malware

Code execution on the container/host, then used to pivot, host or spread malware, or reach other
systems. Blast radius leaves the app.

## D3 — Downtime that drives users away

Prolonged or repeated unavailability until users stop trusting the app and leave. No data lost or
exposed, but abandonment doesn't reverse.
