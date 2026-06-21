#!/usr/bin/env python3
"""Validate STRIDE-per-boundary YAML files against the stride-boundary/v1 format.

See docs/threat-model/stride/README.md for the format.

Usage:
    validate_stride.py [FILE ...]

With no arguments, validates every *.yaml under docs/threat-model/stride/.
Exits non-zero if any file is invalid.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

SCHEMA = "stride-boundary/v1"
REPO_ROOT = Path(__file__).resolve().parent.parent
STRIDE_DIR = REPO_ROOT / "docs" / "threat-model" / "stride"

ELEMENT_TYPES = {"process", "data_flow", "external_entity", "data_store"}

CATEGORIES = {
    "spoofing",
    "tampering",
    "repudiation",
    "information_disclosure",
    "denial_of_service",
    "elevation_of_privilege",
}

# STRIDE per element: (required categories, optional categories) by element type.
CATEGORIES_BY_TYPE = {
    "process": (CATEGORIES, set()),
    "data_flow": ({"tampering", "information_disclosure", "denial_of_service"}, set()),
    "external_entity": ({"spoofing", "repudiation"}, set()),
    "data_store": (
        {"tampering", "information_disclosure", "denial_of_service"},
        {"repudiation"},  # +R if it stores logs
    ),
}

STATUSES = {"handled", "partial", "open", "n/a"}
DDS = {"D1", "D2", "D3"}


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []

    def err(msg: str) -> None:
        errors.append(msg)

    try:
        doc = yaml.safe_load(path.read_text())
    except (yaml.YAMLError, OSError) as exc:
        return [f"could not parse YAML: {exc}"]

    if not isinstance(doc, dict):
        return ["top level must be a mapping"]

    if doc.get("schema") != SCHEMA:
        err(f"schema must be {SCHEMA!r}, got {doc.get('schema')!r}")

    # --- boundary ---------------------------------------------------------
    elements: dict[str, str] = {}  # element id -> type
    boundary = doc.get("boundary")
    if not isinstance(boundary, dict):
        err("missing 'boundary' mapping")
    else:
        for key in ("id", "name", "summary", "left", "right", "flow"):
            if key not in boundary:
                err(f"boundary missing {key!r}")
        for side in ("left", "right"):
            el = boundary.get(side)
            if not isinstance(el, dict):
                err(f"boundary.{side} must be a mapping")
                continue
            for key in ("id", "name", "type"):
                if key not in el:
                    err(f"boundary.{side} missing {key!r}")
            if el.get("type") not in ELEMENT_TYPES:
                err(f"boundary.{side}.type invalid: {el.get('type')!r}")
            if "id" in el:
                elements[el["id"]] = el.get("type")
        flow = boundary.get("flow")
        if not isinstance(flow, dict):
            err("boundary.flow must be a mapping")
        else:
            for key in ("id", "name", "summary"):
                if key not in flow:
                    err(f"boundary.flow missing {key!r}")

    # --- analyses ---------------------------------------------------------
    analyses = doc.get("analyses")
    if not isinstance(analyses, list) or not analyses:
        err("missing non-empty 'analyses' list")
        return errors

    seen_ids: set[str] = set()
    seen_targets: set[str] = set()

    for i, analysis in enumerate(analyses):
        loc = f"analyses[{i}]"
        if not isinstance(analysis, dict):
            err(f"{loc} must be a mapping")
            continue

        target = analysis.get("target")
        atype = analysis.get("type")
        seen_targets.add(target)

        if atype not in ELEMENT_TYPES:
            err(f"{loc}.type invalid: {atype!r}")

        # target must reference 'flow' or a boundary element, with matching type
        if target == "flow":
            if atype != "data_flow":
                err(f"{loc}: target 'flow' must have type 'data_flow'")
        elif target in elements:
            if elements[target] != atype:
                err(
                    f"{loc}: type {atype!r} does not match element "
                    f"{target!r} (declared {elements[target]!r})"
                )
        else:
            err(f"{loc}: target {target!r} is not 'flow' or a boundary element id")

        threats = analysis.get("threats")
        if not isinstance(threats, list) or not threats:
            err(f"{loc} missing non-empty 'threats'")
            continue

        present: set[str] = set()
        for j, threat in enumerate(threats):
            tloc = f"{loc}.threats[{j}]"
            if not isinstance(threat, dict):
                err(f"{tloc} must be a mapping")
                continue

            tid = threat.get("id")
            if not tid:
                err(f"{tloc} missing 'id'")
            elif tid in seen_ids:
                err(f"{tloc} duplicate id {tid!r}")
            else:
                seen_ids.add(tid)

            category = threat.get("category")
            if category not in CATEGORIES:
                err(f"{tloc} invalid category: {category!r}")
            else:
                present.add(category)

            if not threat.get("threat"):
                err(f"{tloc} missing 'threat' text")

            dds = threat.get("dds")
            if not isinstance(dds, list) or not dds:
                err(f"{tloc} 'dds' must be a non-empty list")
            else:
                for d in dds:
                    if d not in DDS:
                        err(f"{tloc} invalid dds {d!r}")

            mitigation = threat.get("mitigation")
            if not isinstance(mitigation, dict):
                err(f"{tloc} missing 'mitigation' mapping")
            else:
                if mitigation.get("status") not in STATUSES:
                    err(f"{tloc} mitigation.status invalid: {mitigation.get('status')!r}")
                if not mitigation.get("notes"):
                    err(f"{tloc} mitigation.notes missing")

            refs = threat.get("refs")
            if refs is not None and not isinstance(refs, list):
                err(f"{tloc} 'refs' must be a list")

        # category completeness for this element type
        if atype in CATEGORIES_BY_TYPE:
            required, optional = CATEGORIES_BY_TYPE[atype]
            missing = required - present
            extra = present - (required | optional)
            if missing:
                err(f"{loc} ({atype}) missing categories: {', '.join(sorted(missing))}")
            if extra:
                err(f"{loc} ({atype}) categories not allowed here: {', '.join(sorted(extra))}")

    # every boundary element + the flow should have an analysis
    if isinstance(boundary, dict):
        expected = {"flow"}
        for side in ("left", "right"):
            el = boundary.get(side)
            if isinstance(el, dict) and "id" in el:
                expected.add(el["id"])
        for missing_target in sorted(expected - seen_targets):
            err(f"no analysis for {missing_target!r}")

    return errors


def main(argv: list[str]) -> int:
    if argv:
        files = [Path(a) for a in argv]
    else:
        files = sorted(STRIDE_DIR.glob("*.yaml")) + sorted(STRIDE_DIR.glob("*.yml"))

    files = [f for f in files if f.suffix in {".yaml", ".yml"}]
    if not files:
        print("No STRIDE YAML files to validate.")
        return 0

    failed = False
    for path in files:
        errors = validate_file(path)
        if errors:
            failed = True
            print(f"FAIL {path}")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"ok   {path}")

    if failed:
        print("\nSTRIDE validation failed.")
        return 1
    print(f"\nAll {len(files)} STRIDE file(s) valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
