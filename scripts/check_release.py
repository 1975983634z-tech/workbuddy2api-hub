#!/usr/bin/env python3
"""Fail when a public source tree contains runtime data or obvious secrets."""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".ruff_cache"}
RUNTIME_ONLY_DIRS = {"catalog", "logs", "suite-logs"}
RUNTIME_EXTENSIONS = {".db", ".sqlite", ".sqlite3", ".jsonl", ".log", ".pem", ".key"}
TEXT_SUFFIXES = {".py", ".html", ".md", ".txt", ".yml", ".yaml", ".json", ".toml", ".ini", ".sh"}
PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})"),
    "Slack token": re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "generic API key": re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}"),
    "known deployment marker": re.compile("|".join(["134\.175\.153\.158", "Zhang" + "0410", "300b" + "3947"])),
}


def iter_files() -> list[Path]:
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def check_path(path: Path) -> list[str]:
    rel = path.relative_to(ROOT)
    errors = []
    parts = set(rel.parts)
    if path.name != "README.md" and "accounts" in parts:
        errors.append(f"runtime account file present: {rel}")
    if path.name != "README.md" and "usage" in parts:
        errors.append(f"runtime usage file present: {rel}")
    if parts & RUNTIME_ONLY_DIRS:
        errors.append(f"runtime directory contains a file: {rel}")
    if path.suffix.lower() in RUNTIME_EXTENSIONS:
        errors.append(f"runtime-sensitive extension present: {rel}")
    if path.name.startswith(".env") and path.name != ".env.example":
        errors.append(f"environment file present: {rel}")
    return errors


def scan_text(path: Path) -> list[str]:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [f"text-like file is not UTF-8: {path.relative_to(ROOT)}"]
    errors = []
    for label, pattern in PATTERNS.items():
        if pattern.search(text):
            errors.append(f"{label} pattern found in {path.relative_to(ROOT)}")
    return errors


def main() -> int:
    errors = []
    files = iter_files()
    for path in files:
        errors.extend(check_path(path))
        errors.extend(scan_text(path))
    if errors:
        print("Release safety check failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(f"Release safety check passed for {len(files)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
