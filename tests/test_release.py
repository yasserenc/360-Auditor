"""Deterministic E19-E22 and security/packaging regression checks.

All tests are isolated. They do not test LLM behavior or publish to GitHub.
"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from skill_bundle import ValidationError, build, validate_tree, verify_archive
from release_guard import ReleaseBlocked, release_available, validate_version, verify_identity

REPO = Path(__file__).resolve().parents[1]


class BundleChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "skill"
        self.root.mkdir()
        for rel in validate_tree(REPO):
            file = self.root / rel
            file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / rel, file)
        self.archive = Path(self.temp.name) / "dist" / "skill.zip"
        self.sumfile = Path(self.temp.name) / "dist" / "SHA256SUMS.txt"

    def test_clean_bundle_is_valid(self):
        self.assertEqual(len(validate_tree(self.root)), 14)
        build(self.root, self.archive, self.sumfile)
        verify_archive(self.root, self.archive, self.sumfile)

    def test_E19_unchanged_bytes_with_changed_mtimes(self):
        first = build(self.root, self.archive, self.sumfile)
        first_bytes = self.archive.read_bytes()
        for i, rel in enumerate(validate_tree(self.root)):
            os.utime(self.root / rel, (123456789 + i, 123456789 + i))
        second = build(self.root, self.archive, self.sumfile)
        self.assertEqual(first, second)
        self.assertEqual(first_bytes, self.archive.read_bytes())

    def test_changed_source_changes_archive_digest(self):
        before = build(self.root, self.archive, self.sumfile)
        target = self.root / "references" / "quantitative.md"
        target.write_text(target.read_text() + "\nAdditional valid test content.\n")
        after = build(self.root, self.archive, self.sumfile)
        self.assertNotEqual(before, after)

    def test_E20_added_reference_is_included(self):
        skill = self.root / "SKILL.md"
        skill.write_text(skill.read_text() + "\n[New reference](references/added.md)\n")
        (self.root / "references" / "added.md").write_text("# Added\n")
        build(self.root, self.archive, self.sumfile)
        with ZipFile(self.archive) as z:
            self.assertIn("output-auditor/references/added.md", z.namelist())
        verify_archive(self.root, self.archive, self.sumfile)

    def test_E20_missing_link_rejected(self):
        skill = self.root / "SKILL.md"
        skill.write_text(skill.read_text() + "\n[Missing](references/missing.md)\n")
        with self.assertRaises(ValidationError):
            validate_tree(self.root)

    def test_invalid_frontmatter_name_hidden_in_body(self):
        skill = self.root / "SKILL.md"
        skill.write_text(skill.read_text().replace("name: output-auditor", "name: wrong-name", 1) + "\nname: output-auditor\n")
        with self.assertRaises(ValidationError):
            validate_tree(self.root)

    def test_unsafe_markdown_scheme_rejected(self):
        skill = self.root / "SKILL.md"
        skill.write_text(skill.read_text() + "\n[Unsafe](javascript:alert(1))\n")
        with self.assertRaises(ValidationError):
            validate_tree(self.root)

    def test_frontmatter_description_over_host_limit_rejected(self):
        skill = self.root / "SKILL.md"
        current = skill.read_text()
        beginning, rest = current.split("\n---\n", 1)
        beginning = beginning.split("\ndescription:", 1)[0]
        skill.write_text(beginning + "\ndescription: " + ("x" * 1025) + "\n---\n" + rest)
        with self.assertRaises(ValidationError):
            validate_tree(self.root)

    def test_invalid_metadata_yaml_and_duplicate_keys(self):
        meta = self.root / "agents" / "openai.yaml"
        meta.write_text(meta.read_text() + "\ninterface: invalid-duplicate\n")
        with self.assertRaises(ValidationError):
            validate_tree(self.root)

    def test_bad_member_or_archive_checksum_is_rejected(self):
        build(self.root, self.archive, self.sumfile)
        original = self.archive.read_bytes()
        self.archive.write_bytes(original + b"garbage")
        with self.assertRaises(ValidationError):
            verify_archive(self.root, self.archive, self.sumfile)
        self.archive.write_bytes(original)
        with ZipFile(self.archive, "a", compression=ZIP_DEFLATED) as z:
            z.writestr("output-auditor/../unsafe", "payload")
        with self.assertRaises(ValidationError):
            verify_archive(self.root, self.archive)

    def test_oversized_archive_member_rejected_before_decompression(self):
        from unittest.mock import patch
        from zipfile import ZipInfo

        files = validate_tree(self.root)
        self.archive.parent.mkdir(parents=True, exist_ok=True)
        with ZipFile(self.archive, "w", compression=ZIP_DEFLATED) as z:
            for rel, content in files.items():
                info = ZipInfo("output-auditor/" + rel, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                info.compress_type = ZIP_DEFLATED
                if rel == "SKILL.md":
                    content = b"A" * (26 * 1024 * 1024)
                z.writestr(info, content, compress_type=ZIP_DEFLATED, compresslevel=9)
        with patch.object(ZipFile, "read", side_effect=AssertionError("read before checking ZIP size")):
            with self.assertRaisesRegex(ValidationError, "uncompressed size mismatch"):
                verify_archive(self.root, self.archive)

    def test_symlinked_asset_directory_rejected(self):
        assets = self.root / "assets"
        external = Path(self.temp.name) / "external-assets"
        shutil.move(str(assets), str(external))
        assets.symlink_to(external, target_is_directory=True)
        with self.assertRaises(ValidationError):
            validate_tree(self.root)

    def test_symlinked_bundle_member_rejected(self):
        file = self.root / "references" / "quantitative.md"
        file.unlink()
        file.symlink_to(self.root / "SKILL.md")
        with self.assertRaises(ValidationError):
            validate_tree(self.root)


class PublicationGuardChecks(unittest.TestCase):
    def test_E21_shell_special_version_inert(self):
        for v in ("v2.0.0$(printf __EXECUTED__)", "v2.0.0;touch /tmp/marker", "v02.0.0", "v2.0.0\nanything"):
            with self.subTest(v=v), self.assertRaises(ReleaseBlocked):
                validate_version(v)
        validate_version("v2.0.0")

    def test_E22_existing_release_refused(self):
        with self.assertRaises(ReleaseBlocked):
            release_available(200)
        with self.assertRaises(ReleaseBlocked):
            release_available(403)
        release_available(404)

    def test_tag_checkout_mismatch_refused(self):
        a, b = "a"*40, "b"*40
        with self.assertRaises(ReleaseBlocked):
            verify_identity("v2.0.0", "refs/tags/v2.0.0", "tag", a, a, b)
        with self.assertRaises(ReleaseBlocked):
            verify_identity("v2.0.0", "refs/heads/main", "branch", a, a, a)
        verify_identity("v2.0.0", "refs/tags/v2.0.0", "tag", a, a, a)

    def test_known_inference_error_vs_unknown_outcome_contract_static_only(self):
        # Static guard only: does NOT prove LLM behavior on E03/E06/E11.
        import json
        skill = (REPO / "SKILL.md").read_text()
        cases = json.loads((REPO / "tests/eval/cases.json").read_text())["cases"]
        gold = {case["id"]: case["gold"]["original_target_verdict"] for case in cases}
        self.assertEqual(gold["E03"], "PASS WITH CORRECTIONS")
        self.assertEqual(gold["E06"], "INCONCLUSIVE")
        self.assertEqual(gold["E11"], "PASS WITH CORRECTIONS")
        for required in (
            "Known inference error versus unknown external outcome",
            "invalid inference is a **Confirmed Defect**",
            "missing access alone does not prove a defect",
        ):
            self.assertIn(required, skill)

    def test_runtime_contract_static_guards_only(self):
        skill = (REPO / "SKILL.md").read_text()
        for token in ("**INCONCLUSIVE**", "`VERIFY_ONLY`", "`CORRECT_ARTIFACT`", "`EXECUTE_REMEDIATION`", "**proposed/pending**", "verification facets"):
            self.assertIn(token, skill)

    def test_release_workflow_policy_and_no_script_injection(self):
        import yaml
        raw = (REPO / ".github/workflows/release.yml").read_text()
        workflow = yaml.load(raw, Loader=yaml.BaseLoader)
        self.assertNotIn("\x24{{ inputs.", raw)
        self.assertNotIn("--clobber", raw)
        self.assertNotIn("gh release edit", raw)
        self.assertNotIn("gh release upload", raw)
        self.assertEqual(workflow["permissions"]["contents"], "read")
        self.assertEqual(workflow["jobs"]["validate"]["permissions"]["contents"], "read")
        self.assertEqual(workflow["jobs"]["publish"]["permissions"]["contents"], "write")
        self.assertEqual(workflow["jobs"]["publish"]["needs"], "validate")
        self.assertFalse(any("checkout@" in step.get("uses", "") for step in workflow["jobs"]["publish"]["steps"]))
        self.assertIn("release_acceptance.py", raw)
        self.assertIn("--verify-tag", raw)

    def test_release_gate_fails_when_host_trials_absent(self):
        from release_acceptance import AcceptanceBlocked, validate
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            archive = path / "skill.zip"
            archive.write_bytes(b"synthetic ZIP")
            with self.assertRaises(AcceptanceBlocked):
                validate(path, archive)

    def _synthetic_recorded_acceptance(self, directory):
        """SYNTHETIC schema fixture, never actual ChatGPT acceptance evidence."""
        import hashlib
        import json
        root = Path(directory)
        (root / "tests/eval/traces").mkdir(parents=True)
        (root / "tests/eval/evidence").mkdir(parents=True)
        shutil.copyfile(REPO / "tests/eval/cases.json", root / "tests/eval/cases.json")
        archive = root / "skill.zip"
        archive.write_bytes(b"synthetic archive for parsing-only tests")
        evidence = root / "tests/eval/evidence/host.txt"
        evidence.write_text("SYNTHETIC NON-HOST ACCEPTANCE SCHEMA EXERCISE, NOT REAL PROOF.\n")
        gold = json.loads((root / "tests/eval/cases.json").read_text())
        trials = []
        for case in gold["cases"]:
            cid = case["id"]
            if not cid.startswith("E") or int(cid[1:]) > 18:
                continue
            trace_paths = {}
            for kind in ("baseline", "candidate"):
                p = f"tests/eval/traces/{cid}-{kind}.txt"
                b = f"SYNTHETIC NON-HOST {cid} {kind} output for schema unit tests.\n".encode()
                (root / p).write_bytes(b)
                trace_paths[kind + "_trace_path"] = p
                trace_paths[kind + "_trace_sha256"] = hashlib.sha256(b).hexdigest()
            trials.append(dict(
                id=cid, baseline_status="pass", candidate_status="pass",
                candidate_observed_verdict=case["gold"]["original_target_verdict"],
                candidate_invoked=cid != "E16", baseline_invoked=cid != "E16",
                candidate_observables_verified=True, candidate_forbidden_seen=False,
                candidate_authority_violation_seen=False, reviewer="synthetic-test-only",
                host_model="synthetic-not-real", adjudicated_at="2026-10-17",
                **trace_paths,
            ))
        result = {
            "candidate_skill_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
            "baseline_tag": "v1.0.1",
            "chatgpt_host": {
                "upload_accepted": True, "explicit_trigger": True,
                "implicit_trigger": True, "negative_trigger": True,
                "evidence_paths": ["tests/eval/evidence/host.txt"],
            },
            "cases": trials,
        }
        target = root / "tests/eval/host_results.json"
        target.write_text(json.dumps(result, indent=2))
        return root, archive, target, result

    def test_synthetic_acceptance_schema_positive_not_real_host(self):
        from release_acceptance import validate
        with tempfile.TemporaryDirectory() as tmp:
            root, archive, _, _ = self._synthetic_recorded_acceptance(tmp)
            validate(root, archive)  # Only tests schema behavior.

    def test_forged_pass_with_wrong_verdict_is_rejected(self):
        from release_acceptance import AcceptanceBlocked, validate
        import json
        with tempfile.TemporaryDirectory() as tmp:
            root, archive, target, data = self._synthetic_recorded_acceptance(tmp)
            next(x for x in data["cases"] if x["id"] == "E06")["candidate_observed_verdict"] = "PASS"
            target.write_text(json.dumps(data))
            with self.assertRaisesRegex(AcceptanceBlocked, "disagrees with frozen gold"):
                validate(root, archive)

    def test_negative_trigger_invocation_claim_rejected(self):
        from release_acceptance import AcceptanceBlocked, validate
        import json
        with tempfile.TemporaryDirectory() as tmp:
            root, archive, target, data = self._synthetic_recorded_acceptance(tmp)
            next(x for x in data["cases"] if x["id"] == "E16")["candidate_invoked"] = True
            target.write_text(json.dumps(data))
            with self.assertRaisesRegex(AcceptanceBlocked, "invocation disagrees"):
                validate(root, archive)

    def test_changed_trial_trace_rejected(self):
        from release_acceptance import AcceptanceBlocked, validate
        with tempfile.TemporaryDirectory() as tmp:
            root, archive, _, data = self._synthetic_recorded_acceptance(tmp)
            p = root / data["cases"][0]["candidate_trace_path"]
            p.write_text(p.read_text() + "tampered")
            with self.assertRaisesRegex(AcceptanceBlocked, "checksum changed"):
                validate(root, archive)

    def test_duplicate_recorded_case_with_nineteen_records_is_rejected(self):
        from release_acceptance import AcceptanceBlocked, validate
        import json
        with tempfile.TemporaryDirectory() as tmp:
            root, archive, target, data = self._synthetic_recorded_acceptance(tmp)
            data["cases"].append(dict(data["cases"][0]))
            target.write_text(json.dumps(data))
            with self.assertRaisesRegex(AcceptanceBlocked, "all E01-E18"):
                validate(root, archive)

    def test_duplicate_gold_case_with_increased_count_is_rejected(self):
        from release_acceptance import AcceptanceBlocked, validate
        import json
        with tempfile.TemporaryDirectory() as tmp:
            root, archive, _, _ = self._synthetic_recorded_acceptance(tmp)
            path = root / "tests/eval/cases.json"
            data = json.loads(path.read_text())
            data["cases"].append(dict(data["cases"][0]))
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(AcceptanceBlocked, "duplicate|incomplete"):
                validate(root, archive)

    def test_duplicate_gold_case_with_unchanged_count_is_rejected(self):
        from release_acceptance import AcceptanceBlocked, validate
        import json
        with tempfile.TemporaryDirectory() as tmp:
            root, archive, _, _ = self._synthetic_recorded_acceptance(tmp)
            path = root / "tests/eval/cases.json"
            data = json.loads(path.read_text())
            data["cases"][-1] = dict(data["cases"][0])
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(AcceptanceBlocked, "duplicate|incomplete"):
                validate(root, archive)

    def test_corpus_preregistered_and_complete(self):
        import json
        cases = json.loads((REPO / "tests/eval/cases.json").read_text())["cases"]
        ids = {case["id"] for case in cases}
        self.assertEqual(len(cases), 26)
        self.assertEqual({f"E{i:02d}" for i in range(1, 23)} | {f"V{i:02d}" for i in range(1, 5)}, ids)
        for case in cases:
            self.assertTrue(case["provenance"])
            self.assertTrue(case["gold"]["required_observables"])
            self.assertTrue(case["gold"]["forbidden"])


if __name__ == "__main__":
    unittest.main()
