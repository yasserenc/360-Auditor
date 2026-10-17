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

    def test_runtime_contract_static_guards_only(self):
        skill = (REPO / "SKILL.md").read_text()
        for token in ("**INCONCLUSIVE**", "`VERIFY_ONLY`", "`CORRECT_ARTIFACT`", "`EXECUTE_REMEDIATION`", "**proposed/pending**", "verification facets"):
            self.assertIn(token, skill)

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
