# Test Coverage Matrix

> **Example prompt:** *"Build the test-coverage matrix. Input: functional-requirements.md, security-requirements.md, and the actual test suite — ask a developer where the tests live or to run them. Don't claim coverage you can't see in the tests. Output: a Markdown table per API mapping every requirement to its positive and negative test cases, with gaps called out."*

Maps each in-scope requirement to its positive (P) and negative (N) test case, per API.
Status: ✅ covered · ⚠️ accepted residual · ❌ gap.

Excluded: config/scaffold-only requirements (SR-2, SR-10, SR-13–15) and deferred production ones
(SR-4, SR-11). SR-7 is task-only (the User row has no `owner`).

## Tasks API

| Requirement | Positive | Negative | Status |
|-------------|----------|----------|--------|
| FR-4 create own | `test_owner_can_create_and_list` | — | ✅ |
| FR-4 retrieve own | `test_owner_can_retrieve_own_task` | — | ✅ |
| FR-4 update own | `test_owner_can_update_own_task` | — | ✅ |
| FR-4 delete own | `test_owner_can_delete_own_task` | `test_cannot_reach_another_users_task` | ✅ |
| FR-5 list own only | `test_owner_can_create_and_list` | `test_list_is_scoped_to_owner` | ✅ |
| FR-6 admin = normal user | — | `test_admin_has_no_api_bypass` | ✅ |
| SR-1 auth required | (authed tests succeed) | `test_anonymous_is_denied` | ✅ |
| SR-5 function perm incl. view | (in-group users succeed) | `test_missing_view_permission_is_forbidden_even_for_owner` | ✅ |
| SR-6 object ownership | — | `test_list_is_scoped_to_owner`, `test_cannot_reach_another_users_task` | ✅ |
| SR-7 owner server-set | — | `test_owner_is_server_set_on_create` | ✅ |
| SR-8 mass-assignment guard | — | `test_owner_cannot_be_reassigned_via_patch` | ✅ |
| SR-9 admin no API bypass | — | `test_admin_has_no_api_bypass` | ✅ |

## Users API

| Requirement | Positive | Negative | Status |
|-------------|----------|----------|--------|
| FR-1 register + email verify | — | — | ⚠️ [RR-1](../threat-model/risk-register.md) |
| FR-2 session + token auth | `test_self_delete_flushes_session` (session), `test_token_authentication_is_accepted` | `test_invalid_token_is_rejected` | ✅ (login/logout flow → [RR-1](../threat-model/risk-register.md)) |
| FR-3 view self | `test_can_retrieve_self`, `test_me` | — | ✅ |
| FR-3 update self | `test_can_update_self` | — | ✅ |
| FR-3 delete self | `test_self_delete_flushes_session` | — | ✅ |
| FR-6 admin = normal user | — | `test_admin_has_no_api_bypass` | ✅ |
| SR-1 auth required | (authed tests succeed) | `test_anonymous_is_denied` | ✅ |
| SR-3 email verify before login | — | — | ⚠️ [RR-1](../threat-model/risk-register.md) |
| SR-5 function perm incl. view | `test_default_group_*` | `test_missing_view_permission_is_forbidden` | ✅ |
| SR-6 object ownership | `test_can_retrieve_self` | `test_list_is_scoped_to_self`, `test_cannot_retrieve_another_user`, `test_get_queryset` | ✅ |
| SR-8 mass-assignment / no escalation | — | `test_cannot_escalate_privilege_via_patch` | ✅ |
| SR-9 admin no API bypass | — | `test_admin_has_no_api_bypass` | ✅ |

## Status

All in-scope FR/SR for both APIs are covered by positive and negative tests, except the allauth-owned
signup/verification/session-login flows, accepted as [RR-1](../threat-model/risk-register.md).
