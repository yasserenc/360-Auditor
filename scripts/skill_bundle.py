#!/usr/bin/env python3
"""Validate and reproducibly package the output-auditor runtime bundle.

This validates repository-specific source structure, not ChatGPT host acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import posixpath
import re
import tempfile
from pathlib import Path, PurePosixPath
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

import yaml

ROOT_NAME = "output-auditor"
MAX_BYTES = 25 * 1024 * 1024
MARKDOWN_LINK = re.compile(r"(?<!!)\]\(([^)]+)\)")
SENSITIVE = re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{30,}|sk-proj-[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{16}")


class ValidationError(ValueError):
    pass


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate mapping keys, which ordinary YAML loaders may overwrite."""


def unique_mapping(loader: UniqueLoader, node: yaml.MappingNode) -> dict:
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if not isinstance(key, str) or key in result:
            raise ValidationError(f"non-string or repeated YAML key: {key!r}")
        result[key] = loader.construct_object(value_node)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def load_yaml(text: str, label: str) -> dict:
    try:
        data = yaml.load(text, Loader=UniqueLoader)
    except yaml.YAMLError as exc:
        raise ValidationError(f"invalid {label} YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValidationError(f"{label}: expected YAML mapping")
    return data


def safe_relative(path: str) -> str:
    if not path or "\\" in path or "\x00" in path or path.startswith("/") or "?" in path:
        raise ValidationError(f"unsafe local path: {path!r}")
    parts = PurePosixPath(path).parts
    if ".." in parts or "." in parts or posixpath.normpath(path) != path:
        raise ValidationError(f"traversal/noncanonical local path: {path!r}")
    return path


def source_bytes(root: Path, rel: str) -> bytes:
    safe_relative(rel)
    file = root / rel
    # Prevent source paths from escaping through a symlinked parent directory.
    current = root
    for part in PurePosixPath(rel).parts:
        current = current / part
        if current.is_symlink():
            raise ValidationError(f"symlinked bundle path component: {rel}")
    if not file.is_file() or file.is_symlink():
        raise ValidationError(f"missing or symlinked bundle file: {rel}")
    data = file.read_bytes()
    if SENSITIVE.search(data):
        raise ValidationError(f"possible credential/private key in bundle: {rel}")
    return data


def markdown_links(text: str, source: str) -> set[str]:
    links = set()
    for raw in MARKDOWN_LINK.findall(text):
        # Internal Skill references have plain relative paths. Links with
        # external URLs, fragments, or mailto are not packaged.
        link = raw.split("#", 1)[0].strip().split(' "', 1)[0]
        if not link or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", link):
            continue
        if link.startswith("//"):
            continue
        # Resolve relative to the Markdown file, then validate canonical root.
        target = posixpath.normpath(posixpath.join(posixpath.dirname(source), link))
        if link.startswith("/") or ".." in PurePosixPath(link).parts or "\\" in link:
            raise ValidationError(f"escaping Markdown link in {source}: {raw!r}")
        links.add(safe_relative(target))
    return links


def validate_tree(root: Path) -> dict[str, bytes]:
    root = root.resolve()
    skill = source_bytes(root, "SKILL.md").decode("utf-8")
    fm = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", skill, flags=re.S)
    if not fm:
        raise ValidationError("SKILL.md missing delimited YAML frontmatter")
    frontmatter = load_yaml(fm.group(1), "SKILL.md frontmatter")
    if set(frontmatter) != {"name", "description"} or frontmatter["name"] != ROOT_NAME:
        raise ValidationError("frontmatter must contain exact name: output-auditor and description")
    description = frontmatter["description"]
    if not isinstance(description, str) or not (90 <= len(description) <= 2000):
        raise ValidationError("description must be a nonempty, meaningful string")
    if "audit" not in description.lower() or "do not trigger" not in description.lower():
        raise ValidationError("frontmatter description needs audit and negative-trigger scope")
    if len(skill[fm.end():].strip()) < 200:
        raise ValidationError("SKILL.md body is empty or implausibly short")

    metadata = load_yaml(source_bytes(root, "agents/openai.yaml").decode("utf-8"), "agents/openai.yaml")
    if not set(metadata).issubset({"interface", "policy"}) or "interface" not in metadata:
        raise ValidationError("unsupported metadata top-level mapping")
    interface = metadata["interface"]
    if not isinstance(interface, dict):
        raise ValidationError("interface metadata is not a mapping")
    for field in ("display_name", "short_description", "default_prompt", "icon_small", "icon_large"):
        if not isinstance(interface.get(field), str) or not interface[field].strip():
            raise ValidationError(f"metadata interface.{field} must be a nonempty string")
    if "policy" in metadata:
        p = metadata["policy"]
        if not isinstance(p, dict) or not set(p).issubset({"allow_implicit_invocation", "products"}):
            raise ValidationError("invalid policy mapping")
        if "allow_implicit_invocation" in p and not isinstance(p["allow_implicit_invocation"], bool):
            raise ValidationError("allow_implicit_invocation must be boolean")
        if "products" in p and (not isinstance(p["products"], list) or not all(isinstance(x, str) and x for x in p["products"])):
            raise ValidationError("policy.products must be a list of strings; host acceptance unverified")

    refs_dir = root / "references"
    if not refs_dir.is_dir() or refs_dir.is_symlink():
        raise ValidationError("references directory absent or symlinked")
    ref_paths = sorted(p.relative_to(root).as_posix() for p in refs_dir.rglob("*"))
    if not ref_paths or any(not p.endswith(".md") or "/" in p[len("references/"):] for p in ref_paths):
        raise ValidationError("references must consist only of flat Markdown files")
    assets = {safe_relative(interface[key]) for key in ("icon_small", "icon_large")}
    if any(not p.startswith("assets/") or not p.endswith(".svg") for p in assets):
        raise ValidationError("icons must be local SVG assets")
    asset_dir = root / "assets"
    assets_present = {p.relative_to(root).as_posix() for p in asset_dir.rglob("*")} if asset_dir.is_dir() else set()
    if assets_present != assets:
        raise ValidationError(f"icon asset closure mismatch, present={assets_present} required={assets}")
    rels = ["SKILL.md", "agents/openai.yaml", *ref_paths, *sorted(assets)]
    files = {rel: source_bytes(root, rel) for rel in rels}
    for rel in ["SKILL.md", *ref_paths]:
        content = files[rel].decode("utf-8")
        for target in markdown_links(content, rel):
            if target not in files:
                raise ValidationError(f"unbundled/broken reference from {rel}: {target}")
    for icon in assets:
        svg = files[icon].decode("utf-8")
        if not svg.lstrip().startswith("<svg") or re.search(r"<script\b|<foreignObject\b|<image\b|<use\b|\bon\w+\s*=|<!DOCTYPE|\bxlink:href\s*=", svg, re.I):
            raise ValidationError(f"unexpected potentially active SVG in {icon}")
    if sum(map(len, files.values())) > MAX_BYTES:
        raise ValidationError("bundle exceeds maximum uncompressed size")
    return dict(sorted(files.items()))


def build(root: Path, archive: Path, checksum: Path) -> str:
    files = validate_tree(root)
    archive.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(archive, mode="w", compression=ZIP_DEFLATED, compresslevel=9, strict_timestamps=True) as z:
        for rel, data in files.items():
            info = ZipInfo(f"{ROOT_NAME}/{rel}", date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = ZIP_DEFLATED
            z.writestr(info, data, compress_type=ZIP_DEFLATED, compresslevel=9)
    verify_archive(root, archive)
    if archive.stat().st_size > MAX_BYTES:
        raise ValidationError("archive exceeds 25 MiB host limit")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum.parent.mkdir(parents=True, exist_ok=True)
    checksum.write_text(f"{digest}  skill.zip\n", encoding="ascii")
    return digest


def verify_archive(root: Path, archive: Path, checksum: Path | None = None) -> None:
    files = validate_tree(root)
    expected = [f"{ROOT_NAME}/{rel}" for rel in files]
    with ZipFile(archive, "r") as z:
        members = z.infolist()
        names = [m.filename for m in members]
        if names != expected or len(names) != len(set(names)):
            raise ValidationError("ZIP manifest mismatch, ordering error or duplicate names")
        for entry, rel in zip(members, files):
            if entry.is_dir() or (entry.external_attr >> 16) != 0o100644:
                raise ValidationError(f"invalid ZIP file mode: {entry.filename}")
            if entry.date_time != (1980, 1, 1, 0, 0, 0) or entry.compress_type != ZIP_DEFLATED:
                raise ValidationError(f"non-reproducible ZIP metadata: {entry.filename}")
            if z.read(entry) != files[rel]:
                raise ValidationError(f"ZIP byte mismatch: {entry.filename}")
        if z.testzip() is not None:
            raise ValidationError("ZIP CRC failed")
        # Validate actual extracted tree, not only repository source files.
        with tempfile.TemporaryDirectory() as temp:
            z.extractall(temp)
            extracted = Path(temp) / ROOT_NAME
            if validate_tree(extracted) != files:
                raise ValidationError("extracted ZIP content failed source validation")
    if checksum is not None:
        expected_line = f"{hashlib.sha256(archive.read_bytes()).hexdigest()}  skill.zip\n"
        if checksum.read_text(encoding="ascii") != expected_line:
            raise ValidationError("SHA256SUMS.txt does not match final archive")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("check", "build", "verify"))
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--archive", type=Path, default=Path("dist/skill.zip"))
    parser.add_argument("--checksum", type=Path, default=Path("dist/SHA256SUMS.txt"))
    args = parser.parse_args()
    if args.mode == "check":
        print(f"validated {len(validate_tree(args.root))} runtime files")
    elif args.mode == "build":
        print(f"skill.zip SHA-256: {build(args.root, args.archive, args.checksum)}")
    else:
        verify_archive(args.root, args.archive, args.checksum)
        print(f"verified archive + checksum: {args.archive}")


if __name__ == "__main__":
    main()
