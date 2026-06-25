# Context Diagram

> **Example prompt:** *"Produce a context diagram for this application. Input: doomsday-scenarios.md and the codebase (backend/). Ask me about anything not evident from the code: the external services it integrates with, the human actors and their roles, and how it is deployed. Don't guess these. Output: a Mermaid flowchart with the app as a single process in the middle and every external entity around it, followed by a short table describing each entity."*

The Todo app as a single monolithic process. External entities that interact with it.

```mermaid
flowchart TB
    users([Users])
    devs([Developers])
    admins([Admins])

    todo[[Todo app]]

    users  -->|create & track own tasks| todo
    devs   -->|build & deploy code| todo
    admins -->|operate & manage| todo
```

| Entity | Role | Interaction |
|--------|------|-------------|
| Users | End users tracking their own tasks | CRUD their own tasks via the API/frontend |
| Developers | Build and ship the app | Commit code, run CI/CD, deploy |
| Admins | Operate and maintain the running system | Infra/DB management, support |

> Entity list is incomplete — more to add.
