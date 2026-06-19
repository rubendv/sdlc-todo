# Functional Requirements (MVP)

Core task tracking. Nothing fancy — enough to implement and run.

| ID | Requirement |
|----|-------------|
| FR-1 | A user can register with email, username, and password. Email verification is mandatory before the account can log in. |
| FR-2 | A user can log in and log out. The API accepts session and token authentication. |
| FR-3 | A user can view, update, and delete their **own** account. |
| FR-4 | A user can create, read, update, and delete their **own** tasks. |
| FR-5 | A user can list their **own** tasks, and only those. |
| FR-6 | Admin: a superuser exists. Via the API an admin behaves as a normal user (own objects only); full access is out-of-band (mechanism TBD). |

## Task model (MVP fields)

| Field | Type | Notes |
|-------|------|-------|
| `title` | string | required |
| `description` | text | optional |
| `completed` | bool | default `false` |
| `owner` | FK(User) | set server-side from the authenticated user |
| `created_at` / `updated_at` | datetime | auto |

Accounts use the existing `User` model (allauth). No new profile fields this iteration.
