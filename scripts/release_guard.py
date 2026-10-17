#!/usr/bin/env python3
"""Fail-closed release identity and published-version guard.

The GitHub Actions publishing job calls this before any public release write.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

VERSION = re.compile(r"v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\Z")
COMMIT = re.compile(r"[a-f0-9]{40}\Z")
REPOSITORY = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")


class ReleaseBlocked(ValueError):
    pass


def validate_version(version: str) -> None:
    if not isinstance(version, str) or not VERSION.fullmatch(version):
        raise ReleaseBlocked("invalid semantic version/tag name")


def verify_identity(version: str, ref: str, ref_type: str, event_sha: str,
                    head_sha: str, tag_commit_sha: str) -> None:
    validate_version(version)
    if ref_type != "tag" or ref != f"refs/tags/{version}":
        raise ReleaseBlocked("release must originate at its exact tag push ref")
    if not all(COMMIT.fullmatch(x) for x in (event_sha, head_sha, tag_commit_sha)):
        raise ReleaseBlocked("invalid Git SHA identity")
    if len({event_sha, head_sha, tag_commit_sha}) != 1:
        raise ReleaseBlocked("tag/checkout/event commit mismatch")


def release_available(status: int) -> None:
    # 404 means an absent release only after the authenticated GitHub REST
    # lookup completed. 403, 500, and network errors must never become "free".
    if status == 200:
        raise ReleaseBlocked("published release already exists; no overwrite permitted")
    if status != 404:
        raise ReleaseBlocked(f"cannot establish release absence (HTTP {status})")


def get_release_status(repo: str, version: str, token: str) -> int:
    if not REPOSITORY.fullmatch(repo) or not token:
        raise ReleaseBlocked("invalid repository or missing release API credentials")
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/releases/tags/{version}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "360-auditor-release-guard"},
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except Exception as exc:
        raise ReleaseBlocked(f"release status unavailable: {exc.__class__.__name__}") from exc


def git_rev_parse(spec: str) -> str:
    try:
        result = subprocess.run(["git", "rev-parse", "--verify", spec],
                                check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        raise ReleaseBlocked(f"git ref could not be resolved: {spec}") from exc
    return result.stdout.strip()


def main() -> int:
    version = os.environ.get("GITHUB_REF_NAME", "")
    try:
        validate_version(version)
        identity = git_rev_parse("HEAD")
        tag_commit = git_rev_parse(f"refs/tags/{version}^{{commit}}")
        verify_identity(version, os.environ.get("GITHUB_REF", ""),
                        os.environ.get("GITHUB_REF_TYPE", ""),
                        os.environ.get("GITHUB_SHA", ""), identity, tag_commit)
        status = get_release_status(os.environ.get("GITHUB_REPOSITORY", ""), version,
                                    os.environ.get("GH_TOKEN", ""))
        release_available(status)
    except ReleaseBlocked as exc:
        print(f"release blocked: {exc}", file=sys.stderr)
        return 1
    print(f"release allowed: {version} -> {identity}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
