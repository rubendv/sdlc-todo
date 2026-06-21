# STRIDE per trust boundary — YAML format

One YAML file per trust boundary, so the analyses stay maintainable and scriptable (validate
completeness, aggregate threats, cross-check the risk register). This replaces the shallow per-boundary
tables in [stride-analysis.md](../stride-analysis.md) as boundaries are migrated here.

## Method: STRIDE per element

A boundary connects two elements with a data flow crossing it. We run three analyses per boundary —
the **left** element, the **flow**, and the **right** element — and the applicable STRIDE categories
depend on each element's type:

| Element type | Categories |
|--------------|-----------|
| `process` | spoofing, tampering, repudiation, information_disclosure, denial_of_service, elevation_of_privilege |
| `data_flow` | tampering, information_disclosure, denial_of_service |
| `external_entity` | spoofing, repudiation |
| `data_store` | tampering, information_disclosure, denial_of_service (+ repudiation if it stores logs) |

By convention the **left** element is the system component (usually a `process`); the **right** is the
other end, which may be a `process` or an `external_entity`.

## Schema (`stride-boundary/v1`)

```yaml
schema: stride-boundary/v1

boundary:
  id: user-api                     # file name matches this id
  name: User ↔ API
  summary: >-
    One or two lines on what crosses here and why it matters.
  left:  { id: api,  name: Todo API, type: process }
  right: { id: user, name: User,     type: external_entity }
  flow:
    id: api-traffic
    name: API request/response
    summary: >-
      What data flows across the boundary.

analyses:
  - target: api                    # an element id, or "flow"
    type: process                  # process | data_flow | external_entity | data_store
    threats:
      - id: user-api/api/S         # boundary/element/category-initial, suffix if >1
        category: spoofing
        threat: >-
          An attacker could <action> in order to <goal>, leading to <impact>.
        dds: [D1]                  # doomsday scenarios: D1 | D2 | D3
        mitigation:
          status: partial          # handled | partial | open | n/a
          notes: >-
            What is in place and what is still missing.
        refs: [RR-7, CWE-639]      # optional: risk-register IDs, CWEs, etc.
```

## Conventions

- **One threat per applicable category** at minimum; add more (suffix the id) when a category splits.
- `status`: `handled` · `partial` · `open` · `n/a`.
- `dds`: every threat maps to at least one doomsday scenario; a threat with no DDS path is out of scope.
- `refs`: link to [risk-register](../risk-register.md) entries (RR-n) and CWEs where useful.
- **Ratings (likelihood/impact) are not done yet** (threat-model backlog). When added, each threat gets
  an optional `rating: { likelihood: <low|med|high>, impact: <low|med|high> }`; omitted until then.

## Boundaries

- [user-api.yaml](user-api.yaml) — User ↔ API (the Internet perimeter). *Done.*
