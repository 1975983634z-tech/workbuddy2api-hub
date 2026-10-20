#!/usr/bin/env python3
"""Build clean source archives without git metadata or runtime data."""

from __future__ import annotations

from pathlib import Path
import hashlib
import subprocess
import sys
import tarfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
DIST = ROOT / "dist"
PREFIX = f"workbuddy2api-hub-{VERSION}"
EXCLUDED_PARTS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".ruff_cache", "dist"}



def included(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if any(part in EXCLUDED_PARTS for part in rel.parts):
        return False
    if path.name != "README.md" and "accounts" in rel.parts:
        return False
    if path.name != "README.md" and "usage" in rel.parts:
        return False
    if {"catalog", "logs", "suite-logs"} & set(rel.parts):
        return False
    if path.name.startswith(".env") and path.name != ".env.example":
        return False
    if path.suffix.lower() in {".db", ".sqlite", ".sqlite3", ".jsonl", ".log", ".pem", ".key"}:
        return False
    return True


def files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*") if path.is_file() and included(path))


def reset() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts/check_release.py")], check=True)
    if DIST.exists():
        for path in DIST.iterdir():
            if path.is_file():
                path.unlink()
    DIST.mkdir(exist_ok=True)


def build() -> list[Path]:
    reset()
    selected = files()
    zip_path = DIST / f"{PREFIX}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in selected:
            archive.write(path, PREFIX + "/" + path.relative_to(ROOT).as_posix())

    tar_path = DIST / f"{PREFIX}.tar.gz"
    with tarfile.open(tar_path, "w:gz") as archive:
        for path in selected:
            archive.add(path, arcname=PREFIX + "/" + path.relative_to(ROOT).as_posix(), recursive=False)

    outputs = [zip_path, tar_path]
    sums = DIST / "SHA256SUMS"
    lines = []
    for path in outputs:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.name}")
    newline = chr(10)
    sums.write_text(newline.join(lines) + newline, encoding="utf-8")
    outputs.append(sums)
    for path in outputs:
        print(path)
    return outputs


if __name__ == "__main__":
    build()
