#!/usr/bin/env python3
"""Syntax-check every notebook's code cells with ast.parse().

This is what docs/code_quality_report.csv (from 18_repository_packaging.ipynb)
already does per-problem at packaging time; this script generalizes it into
a reusable, root-level CI step that runs across every ProblemN_.../notebooks/
folder in the repo, so new phases pick it up automatically without adding a
new CI step per problem.

Usage:
    python scripts/check_notebook_syntax.py [path-to-repo-root]

Exit code 0 if every code cell in every discovered .ipynb parses cleanly;
1 otherwise, with each failure printed as `<file> :: cell <n> :: <error>`.
"""
import ast
import json
import sys
from pathlib import Path


def check_notebook(path: Path) -> list:
    """Return a list of (cell_index, error_message) for any code cell in
    `path` that fails ast.parse(). An empty list means the notebook is
    clean."""
    errors = []
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)
    for i, cell in enumerate(nb.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        if not source.strip():
            continue
        try:
            ast.parse(source, filename=str(path))
        except SyntaxError as exc:
            errors.append((i, f"{exc.__class__.__name__}: {exc.msg} (line {exc.lineno})"))
    return errors


def main() -> int:
    repo_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    notebooks = sorted(repo_root.glob("Problem*_*/notebooks/*.ipynb"))
    if not notebooks:
        print(f"No notebooks found under {repo_root}/Problem*_*/notebooks/ -- nothing to check.")
        return 0

    total_failures = 0
    for nb_path in notebooks:
        errors = check_notebook(nb_path)
        if errors:
            total_failures += len(errors)
            for cell_idx, msg in errors:
                print(f"{nb_path} :: cell {cell_idx} :: {msg}")
        else:
            print(f"OK   {nb_path}")

    print(f"\nChecked {len(notebooks)} notebook(s), {total_failures} syntax error(s).")
    return 1 if total_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
