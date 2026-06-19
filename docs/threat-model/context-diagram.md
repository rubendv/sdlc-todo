# Context Diagram

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
