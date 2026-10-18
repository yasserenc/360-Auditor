"""Exercise the actual GitHub Actions publish shell step against an inert CLI stub.

This test never contacts GitHub and never creates a real tag/release.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]

FAKE_GH = r'''#!/usr/bin/env python3
import json
import os
import sys

argv = sys.argv[1:]
with open(os.environ["FAKE_GH_LOG"], "a", encoding="utf8") as log:
    log.write(json.dumps(argv) + "\n")

if argv[:1] == ["api"]:
    endpoint = next((arg for arg in argv[1:] if arg.startswith("repos/")), "")
    query = argv[-1] if "--jq" in argv else ""
    if "/git/ref/tags/" in endpoint:
        if query == ".object.type":
            print(os.environ.get("FAKE_TAG_TYPE", "commit"))
        elif query == ".object.sha":
            print(os.environ.get("FAKE_TAG_OBJECT_SHA",
                                 os.environ.get("FAKE_TAG_COMMIT_SHA", "")))
        else:
            sys.exit(3)
        sys.exit(0)
    if "/git/tags/" in endpoint:
        if query == ".object.sha":
            print(os.environ.get("FAKE_TAG_COMMIT_SHA", ""))
            sys.exit(0)
        sys.exit(3)
    if "/releases/tags/" in endpoint and "-i" in argv:
        status = os.environ.get("FAKE_RELEASE_STATE", "absent")
        if status == "absent":
            print("HTTP/2.0 404 Not Found")
            sys.exit(1)
        if status == "exists":
            print("HTTP/2.0 200 OK")
            sys.exit(0)
        if status == "forbidden":
            print("HTTP/2.0 403 Forbidden")
            sys.exit(1)
        sys.exit(3)
if argv[:2] == ["release", "create"]:
    sys.exit(0)

print("Unrecognized fake gh call", file=sys.stderr)
sys.exit(3)
'''


class ActualPublishShellTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        workflow = yaml.load((REPO / ".github/workflows/release.yml").read_text(),
                             Loader=yaml.BaseLoader)
        steps = workflow["jobs"]["publish"]["steps"]
        scripts = [step["run"] for step in steps
                   if step.get("name") == "Publish exactly one never-before-published version"]
        if len(scripts) != 1:
            raise AssertionError("exact publish script not found in GitHub workflow")
        cls.publish_script = scripts[0]

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "dist").mkdir()
        (self.root / "dist" / "skill.zip").write_bytes(b"inert candidate")
        (self.root / "dist" / "SHA256SUMS.txt").write_text("a" * 64 + "  skill.zip\n")
        stub = self.root / "gh"
        stub.write_text(FAKE_GH)
        stub.chmod(0o700)
        self.log = self.root / "fake-gh.jsonl"
        sha = "a" * 40
        self.env = dict(os.environ)
        self.env.update({
            "PATH": f"{self.root}:{os.environ['PATH']}",
            "GITHUB_REPOSITORY": "yasserenc/360-Auditor",
            "GITHUB_SHA": sha,
            "VERSION": "v2.0.0",
            "GH_TOKEN": "local-stub-not-real",
            "FAKE_GH_LOG": str(self.log),
            "FAKE_TAG_COMMIT_SHA": sha,
            "FAKE_TAG_OBJECT_SHA": sha,
            "FAKE_TAG_TYPE": "commit",
            "FAKE_RELEASE_STATE": "absent",
        })

    def execute(self):
        result = subprocess.run(["bash", "-c", self.publish_script],
                                cwd=self.root, env=self.env,
                                capture_output=True, text=True, timeout=10)
        calls = [json.loads(line) for line in self.log.read_text().splitlines()] if self.log.exists() else []
        release_calls = [call for call in calls if call[:2] == ["release", "create"]]
        return result, calls, release_calls

    def test_inert_new_tag_calls_create_once_and_no_clobber(self):
        result, calls, releases = self.execute()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(len(releases), 1)
        self.assertIn("--verify-tag", releases[0])
        self.assertNotIn("--clobber", releases[0])
        self.assertIn("--target", releases[0])
        self.assertEqual(releases[0][releases[0].index("--target") + 1], self.env["GITHUB_SHA"])
        notes = (self.root / "tmp-not-needed")
        self.assertTrue(any("/releases/tags/" in " ".join(x) for x in calls))

    def test_existing_published_tag_refuses_without_create(self):
        self.env["FAKE_RELEASE_STATE"] = "exists"
        result, calls, releases = self.execute()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(releases, [])
        self.assertIn("already exists", result.stderr)

    def test_api_error_refuses_without_create(self):
        self.env["FAKE_RELEASE_STATE"] = "forbidden"
        result, calls, releases = self.execute()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(releases, [])
        self.assertIn("cannot confirm", result.stderr)

    def test_changed_tag_commit_refuses_without_create(self):
        self.env["FAKE_TAG_COMMIT_SHA"] = "b" * 40
        self.env["FAKE_TAG_OBJECT_SHA"] = "b" * 40
        result, calls, releases = self.execute()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(releases, [])
        self.assertIn("tag ref changed", result.stderr)

    def test_annotated_tag_dereferences_correctly(self):
        self.env["FAKE_TAG_TYPE"] = "tag"
        self.env["FAKE_TAG_OBJECT_SHA"] = "b" * 40
        result, calls, releases = self.execute()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(len(releases), 1)
        self.assertTrue(any("/git/tags/" in " ".join(x) for x in calls))

    def test_shell_special_version_is_never_evaluated(self):
        marker = self.root / "SHOULD_NOT_EXIST"
        self.env["VERSION"] = f"v2.0.0$(touch {marker})"
        result, calls, releases = self.execute()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(marker.exists())
        self.assertEqual(calls, [])
        self.assertEqual(releases, [])


if __name__ == "__main__":
    unittest.main()
