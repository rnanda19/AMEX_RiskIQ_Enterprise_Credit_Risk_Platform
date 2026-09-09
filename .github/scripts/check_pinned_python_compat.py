#!/usr/bin/env python3
"""Guard against a real bug class this project hit once (Problems 5/6, found
2026-09-09): a `requirements-api.txt` pin whose own PyPI metadata requires a
newer Python than the paired Dockerfile's base image actually ships. That
exact mismatch (xgboost==3.3.0, Requires-Python >=3.12, inside a
python:3.11-slim image) broke the real `docker build` step in CI the first
time these Dockerfiles were ever build-tested with real registry access --
see ROADMAP.md's "Problems 5/6 docker build failure" writeup for the full
root-cause history.

This script closes that gap by checking it here -- fast, offline of Docker,
before a `docker build` ever runs -- instead of relying on a live CI
docker-build failure to notice the next one.

For every `Problem*/src/docker/Dockerfile` in the repo:
  1. Read its `FROM python:X.Y[-slim]` line -> the Dockerfile's target
     Python version.
  2. Resolve the requirements file its `COPY .../requirements-api.txt .`
     line names (tried against the few real build-context conventions this
     repo actually uses, since different problems use different contexts --
     see docker-verify.yml).
  3. For every exact `pkg==version` pin in that file, ask PyPI's own JSON
     API what Python versions that exact release supports
     (`info.requires_python`), and check it against the Dockerfile's
     target Python version.
  4. Print, and fail on, every pin that would break `pip install` inside
     that Dockerfile, and every pin that doesn't exist on PyPI at all.

Network-dependent by design (calls pypi.org) -- "does this exact version
support this Python" is PyPI's own ground truth, not something derivable
from the pin text alone. A transient PyPI/network error on one package is a
warning, not a failure, so a flaky network call can't block a push; a real
`>=3.12`-on-`3.11-slim` style mismatch, or a version that plain doesn't
exist, always fails the check.
"""

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import InvalidVersion, Version

REPO_ROOT = Path(__file__).resolve().parents[2]
PIN_RE = re.compile(r"^([A-Za-z0-9_.\-]+)==([A-Za-z0-9_.\-]+)\s*$")
FROM_RE = re.compile(r"^FROM\s+python:(\d+\.\d+)", re.MULTILINE)
COPY_RE = re.compile(r"^COPY\s+(\S*requirements-api\.txt)\s+", re.MULTILINE)


def find_dockerfiles():
    return sorted(REPO_ROOT.glob("*/src/docker/Dockerfile"))


def resolve_requirements_path(dockerfile_path: Path, copy_src: str):
    docker_dir = dockerfile_path.parent  # .../src/docker
    src_dir = docker_dir.parent  # .../src
    problem_dir = src_dir.parent  # .../ProblemN_.../
    for candidate in (src_dir / copy_src, problem_dir / copy_src, docker_dir / copy_src):
        if candidate.is_file():
            return candidate
    return None


def get_requires_python(pkg: str, version: str):
    """Returns (requires_python_or_None, status) where status is one of
    "ok", "missing" (version doesn't exist on PyPI), or "error" (network/
    parse problem -- treated as non-fatal)."""
    url = f"https://pypi.org/pypi/{pkg}/{version}/json"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None, "missing"
        return None, "error"
    except Exception:
        return None, "error"
    return data.get("info", {}).get("requires_python"), "ok"


def main() -> int:
    dockerfiles = find_dockerfiles()
    if not dockerfiles:
        print("No Problem*/src/docker/Dockerfile files found -- nothing to check.")
        return 0

    violations = []
    warnings = []
    checked = 0

    for dockerfile in dockerfiles:
        text = dockerfile.read_text()
        from_match = FROM_RE.search(text)
        copy_match = COPY_RE.search(text)
        if not from_match or not copy_match:
            continue
        py_ver = from_match.group(1)
        req_path = resolve_requirements_path(dockerfile, copy_match.group(1))
        if req_path is None:
            warnings.append(
                f"{dockerfile.relative_to(REPO_ROOT)}: could not resolve requirements file '{copy_match.group(1)}'"
            )
            continue

        for line in req_path.read_text().splitlines():
            line = line.split("#", 1)[0].strip()
            pin = PIN_RE.match(line)
            if not pin:
                continue
            pkg, version = pin.group(1), pin.group(2)
            checked += 1
            requires_python, status = get_requires_python(pkg, version)

            if status == "missing":
                violations.append(f"{req_path.relative_to(REPO_ROOT)}: {pkg}=={version} does not exist on PyPI at all")
                continue
            if status == "error" or not requires_python:
                if status == "error":
                    warnings.append(
                        f"{req_path.relative_to(REPO_ROOT)}: could not verify {pkg}=={version} against PyPI (network/parse issue) -- not treated as a failure"
                    )
                continue

            try:
                spec = SpecifierSet(requires_python)
                target = Version(f"{py_ver}.0")
                if not spec.contains(target, prereleases=True):
                    violations.append(
                        f"{req_path.relative_to(REPO_ROOT)}: {pkg}=={version} requires Python "
                        f"{requires_python}, but {dockerfile.relative_to(REPO_ROOT)} uses python:{py_ver}-slim"
                    )
            except (InvalidSpecifier, InvalidVersion) as exc:
                warnings.append(
                    f"{req_path.relative_to(REPO_ROOT)}: could not parse requires_python={requires_python!r} for {pkg}=={version}: {exc}"
                )

    print(f"Checked {checked} pinned package(s) across {len(dockerfiles)} Dockerfile(s).")
    for w in warnings:
        print(f"WARN: {w}")

    if violations:
        print("\nFAIL -- pinned dependency / Dockerfile Python-version mismatches found:\n")
        for v in violations:
            print(f"  - {v}")
        return 1

    print("OK -- every pinned package in every requirements-api.txt supports its Dockerfile's Python version.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
