#!/usr/bin/env python3
"""Require evidence for host acceptance and matched behavioral cases before tagging.

Not a replacement for independent human/host verification of raw traces.
"""
import hashlib
import json
import re
import sys
from pathlib import Path


class AcceptanceBlocked(ValueError):
    pass


def validate(root: Path, archive: Path) -> None:
    result_file = root / "tests/eval/host_results.json"
    if not result_file.is_file():
        raise AcceptanceBlocked("P10/P12 host_results.json absent: do not publish")
    result = json.loads(result_file.read_text(encoding="utf-8"))
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if result.get("candidate_skill_sha256") != digest or result.get("baseline_tag") != "v1.0.1":
        raise AcceptanceBlocked("host evidence is not bound to exact candidate ZIP and baseline")
    acceptance = result.get("chatgpt_host", {})
    for field in ("upload_accepted", "explicit_trigger", "implicit_trigger", "negative_trigger"):
        if acceptance.get(field) is not True:
            raise AcceptanceBlocked(f"P10 host check not established: {field}")
    evidence = acceptance.get("evidence_paths")
    if not isinstance(evidence, list) or not evidence:
        raise AcceptanceBlocked("missing host acceptance evidence paths")
    recorded = result.get("cases", [])
    if not isinstance(recorded, list) or len(recorded) != 18:
        raise AcceptanceBlocked("all E01-E18 matched baseline/candidate records required")
    if {x.get("id") for x in recorded if isinstance(x, dict)} != {f"E{i:02d}" for i in range(1, 19)}:
        raise AcceptanceBlocked("incorrect E01-E18 case coverage")
    paths = set(evidence)
    for x in recorded:
        if x.get("candidate_status") != "pass" or x.get("baseline_status") not in ("pass", "fail"):
            raise AcceptanceBlocked(f"unverified/new critical failure in {x['id']}")
        if not x.get("reviewer") or not x.get("host_model"):
            raise AcceptanceBlocked(f"missing provenance for {x['id']}")
        for key in ("baseline_trace_path", "candidate_trace_path"):
            if not isinstance(x.get(key), str) or not x[key].startswith("tests/eval/traces/"):
                raise AcceptanceBlocked(f"missing raw {key} for {x['id']}")
            paths.add(x[key])
    for p in paths:
        if not isinstance(p, str) or not re.fullmatch(r"tests/eval/(?:traces|evidence)/[A-Za-z0-9_./-]+", p):
            raise AcceptanceBlocked(f"invalid evidence path: {p!r}")
        file = root / p
        if ".." in Path(p).parts or not file.is_file() or file.is_symlink() or file.stat().st_size < 32:
            raise AcceptanceBlocked(f"missing or implausibly empty raw evidence: {p}")
    # Automated checks prove a recorded-evidence gate only. Review the actual
    # screenshots/tool traces separately for authenticity and case correctness.


if __name__ == "__main__":
    try:
        validate(Path("."), Path("dist/skill.zip"))
    except (AcceptanceBlocked, ValueError, KeyError, OSError) as exc:
        print(f"RELEASE BLOCKED: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("Recorded host acceptance and matched behavioral evidence gate passed")
