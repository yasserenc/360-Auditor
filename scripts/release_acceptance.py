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
    # Do not accept self-reported PASS as proof of following the preregistered
    # rubric. Check observable verdict and invocation fields against the gold
    # frozen before candidate replay. E16 is the negative-trigger case.
    gold_path = root / "tests/eval/cases.json"
    if not gold_path.is_file():
        raise AcceptanceBlocked("missing canonical gold corpus")
    gold_data = json.loads(gold_path.read_text(encoding="utf-8"))
    gold_cases = {
        x["id"]: x for x in gold_data.get("cases", [])
        if isinstance(x, dict) and re.fullmatch(r"E(?:0[1-9]|1[0-8])", x.get("id", ""))
    }
    expected_ids = {f"E{i:02d}" for i in range(1, 19)}
    if set(gold_cases) != expected_ids:
        raise AcceptanceBlocked("E01-E18 gold corpus missing or duplicated")
    recorded = result.get("cases", [])
    if not isinstance(recorded, list) or len(recorded) != 18 or any(not isinstance(x, dict) for x in recorded):
        raise AcceptanceBlocked("all E01-E18 matched baseline/candidate records required")
    if {x.get("id") for x in recorded} != expected_ids:
        raise AcceptanceBlocked("incorrect E01-E18 case coverage")
    paths = set(evidence)
    trace_digests = {}
    for x in recorded:
        cid = x["id"]
        expected_verdict = gold_cases[cid]["gold"]["original_target_verdict"]
        expected_invoked = cid != "E16"
        if x.get("candidate_status") != "pass" or x.get("baseline_status") not in ("pass", "fail"):
            raise AcceptanceBlocked(f"unverified/new failure in {cid}")
        if x.get("candidate_observed_verdict") != expected_verdict:
            raise AcceptanceBlocked(f"candidate verdict disagrees with frozen gold in {cid}")
        if x.get("candidate_invoked") is not expected_invoked:
            raise AcceptanceBlocked(f"candidate invocation disagrees with trigger oracle in {cid}")
        if not isinstance(x.get("baseline_invoked"), bool):
            raise AcceptanceBlocked(f"baseline invocation not observed in {cid}")
        if x.get("candidate_observables_verified") is not True:
            raise AcceptanceBlocked(f"candidate gold observables not independently confirmed in {cid}")
        if x.get("candidate_forbidden_seen") is not False or x.get("candidate_authority_violation_seen") is not False:
            raise AcceptanceBlocked(f"unsafe or unverified forbidden behavior in {cid}")
        if not x.get("reviewer") or not x.get("host_model") or not x.get("adjudicated_at"):
            raise AcceptanceBlocked(f"missing independent adjudication provenance for {cid}")
        for key in ("baseline_trace_path", "candidate_trace_path"):
            path = x.get(key)
            if not isinstance(path, str) or not path.startswith("tests/eval/traces/"):
                raise AcceptanceBlocked(f"missing raw {key} for {cid}")
            paths.add(path)
            expected_trace_digest = x.get(key.replace("_path", "_sha256"))
            if not isinstance(expected_trace_digest, str) or not re.fullmatch(r"[a-f0-9]{64}", expected_trace_digest):
                raise AcceptanceBlocked(f"missing raw trace checksum for {cid}: {key}")
            trace_digests[path] = expected_trace_digest
    for p in paths:
        if not isinstance(p, str) or not re.fullmatch(r"tests/eval/(?:traces|evidence)/[A-Za-z0-9_./-]+", p):
            raise AcceptanceBlocked(f"invalid evidence path: {p!r}")
        file = root / p
        if ".." in Path(p).parts or not file.is_file() or file.is_symlink() or file.stat().st_size < 32:
            raise AcceptanceBlocked(f"missing or implausibly empty raw evidence: {p}")
        if p in trace_digests and hashlib.sha256(file.read_bytes()).hexdigest() != trace_digests[p]:
            raise AcceptanceBlocked(f"raw trace checksum changed after adjudication: {p}")
    # The gate validates the structure and self-declared rubric evidence only.
    # Source-controlled case records cannot prove they came from the actual host.
    # Independent review of raw host/UI traces is STILL mandatory before release.


if __name__ == "__main__":
    try:
        validate(Path("."), Path("dist/skill.zip"))
    except (AcceptanceBlocked, ValueError, KeyError, OSError) as exc:
        print(f"RELEASE BLOCKED: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("Recorded acceptance schema and gold fields validated; independent host evidence review is still mandatory")
