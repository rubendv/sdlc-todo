# Context Diagram

> **Example prompt:** *"Produce a context diagram for this application. Input: doomsday-scenarios.md and the codebase (backend/). Ask me about the actors and external systems, and which of them we will fully threat-model: include a system as an external entity here only if we will NOT run a full STRIDE analysis on it — systems we intend to fully analyze are modeled as processes in the level-1 DFD instead. Don't guess. Output: a Mermaid flowchart with the app as a single process in the middle and the external entities around it, followed by a short table describing each."*

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
