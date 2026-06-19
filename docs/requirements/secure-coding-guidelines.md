# Secure Coding Guidelines (MVP)

Concrete rules for this codebase, one per CWE in the [shortlist](../threat-model/attack-trees.md).
Default stance: **deny by default, make trust explicit**. Each rule cites its CWE and the doomsday
scenario it guards. Keep these green in review and in tests.

## 1. Object-level authorization — CWE-639 / CWE-862 (D1)

- Every viewset scopes `get_queryset()` to `request.user`. No view returns a global queryset.
- Object endpoints also implement `has_object_permission()` (`IsOwner`); never rely on the queryset alone.
- Never trust a client-supplied id, username, or `owner` to select or filter records.
- Each owner-scoped endpoint gets a negative test: user A cannot reach user B's object.

## 2. Function-level authorization — CWE-285 / CWE-863 (D1)

- Keep `DjangoModelPermissions` (subclassed to require `view_*` on reads) in the default permission
  classes. A missing model permission is a 403, even for the owner.
- Don't grant perms ad hoc in code; assign them through the default `users` group.
- No endpoint sets `permission_classes = [AllowAny]` without a written reason.

## 3. Mass assignment — CWE-915 (D1)

- Serializers list fields explicitly. Never `fields = "__all__"`.
- `owner`, `is_staff`, `is_superuser`, `is_active`, `groups`, `user_permissions` are `read_only`.
- Set `owner` in `perform_create()` from `request.user`, never from request data.

## 4. Sensitive-data & error exposure — CWE-200 / CWE-209 (D1)

- Serializers expose an allowlist of fields; no password, token, or internal flag ever serialized.
- Don't put secrets or PII in logs or error messages.
- `DEBUG = True` is local-only. Never enable it on shared/remote environments (the verbose error
  page leaks settings and stack traces).

## 5. SQL injection — CWE-89 (D1)

- Use the ORM. No `.raw()`, `.extra()`, or `cursor.execute()` with string-built SQL.
- If raw SQL is unavoidable, use parameterized queries (`%s` params), never f-strings or `.format()`.

## 6. Cross-site scripting — CWE-79 (D1)

- API responses are JSON via DRF; never render user content into HTML server-side.
- Never `mark_safe()` or `|safe` on user-supplied data; keep template autoescaping on.
- The frontend must treat task content as untrusted and escape on render.

## 7. Insecure deserialization — CWE-502 (D2)

- Parse input only through DRF's JSON parser. No `pickle`, no `yaml.load` (use `yaml.safe_load`).
- Never deserialize data from the client or cache into Python objects via unsafe loaders.

## 8. OS command injection — CWE-78 (D2)

- Don't shell out with user input. Avoid `os.system`; if `subprocess` is needed, pass an argument
  list and never `shell=True`.

## 9. SSRF — CWE-918 (D2)

- The server does not fetch user-supplied URLs in the MVP. If that changes: allowlist hosts, and
  block internal ranges and the cloud metadata endpoint.

## 10. Authentication & session handling — CWE-287 / CWE-384 / CWE-613 (D1)

- Use allauth and DRF auth. Don't hand-roll login, password reset, or token logic.
- Rotate the session on login; expire/revoke tokens on password change and logout (see
  [access-control](../threat-model/access-control.md) → To decide).

## 11. Cross-origin policy — CWE-942 (D1)

- Do not enable CORS. The frontend is served same-origin via the reverse proxy; `corsheaders` stays removed.
- If a cross-origin client is ever genuinely needed: allowlist exact origins, never reflect the
  `Origin` header, and never combine `Access-Control-Allow-Origin: *` with credentials.

---

Parked: file-upload handling (CWE-22 / CWE-434) — no uploads in the MVP.
