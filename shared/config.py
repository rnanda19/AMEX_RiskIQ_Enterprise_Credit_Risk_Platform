"""Platform config loading -- generalized from the "SECTION 1: ENVIRONMENT
SETUP" boilerplate that is currently duplicated, near-verbatim, at the top
of every notebook in this platform (see e.g. Problem1_Credit_Scoring_
PD_Prediction/notebooks/05_model_development.ipynb, Section 1).

Every notebook in this platform:
  1. Loads artifacts/project_config.json (written by 01_business_understanding.ipynb)
  2. Resolves WARP_THREAD_COUNT (95% of logical cores) and MAX_RAM_BYTES
     (90% of detected RAM) from its `resource_limits` block, falling back
     gracefully on an older config that predates that block
  3. Resolves PILLAR_DIRS -- one output directory per pipeline stage

This module makes that pattern a single, tested function instead of copied
inline logic. Existing notebooks are not yet wired to call this (see
shared/__init__.py) -- this is the extraction step; the notebook rewiring
is a separate, explicitly staged follow-up.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Optional


class PlatformConfig:
    """Resolved platform configuration for one notebook/service run."""

    def __init__(
        self,
        project_config: Dict[str, Any],
        project_root: Path,
        artifacts_dir: Path,
    ) -> None:
        self.raw = project_config
        self.project_root = project_root
        self.artifacts_dir = artifacts_dir

        self.pillar_dirs: Dict[str, Path] = {
            k: Path(v) for k, v in project_config["pillar_dirs"].items()
        }
        self.detected_logical_cores: int = project_config["hardware"]["logical_cores_detected"]
        self.random_seed: int = project_config["random_seed"]

        resource_limits = project_config.get("resource_limits", {})
        self.warp_thread_count: int = (
            resource_limits.get("warp_thread_count")
            or project_config.get("warp_thread_count")
            or self.detected_logical_cores
        )
        self.max_ram_bytes: Optional[int] = resource_limits.get("max_ram_bytes")

    def pillar_dir(self, name: str) -> Path:
        """Look up a pillar output directory by name, e.g. 'model_development'.

        Raises KeyError with the available names if `name` isn't present --
        deliberately not a silent .get() default, since a missing pillar dir
        means an earlier notebook hasn't been run yet (the real failure mode
        this is meant to surface loudly).
        """
        if name not in self.pillar_dirs:
            raise KeyError(
                f"Unknown pillar '{name}'. Available: {sorted(self.pillar_dirs)}"
            )
        return self.pillar_dirs[name]


def load_platform_config(
    project_root: Path | str,
    required_summaries: Optional[Iterable[str]] = None,
) -> "tuple[PlatformConfig, Dict[str, Dict[str, Any]]]":
    """Load artifacts/project_config.json plus any prior-notebook summary
    JSONs a notebook depends on.

    Parameters
    ----------
    project_root:
        The platform's PROJECT_ROOT (contains an `artifacts/` folder).
    required_summaries:
        Names of prior notebooks whose summary JSON this run needs, e.g.
        ("notebook_02_summary", "notebook_04_summary"). Each is loaded from
        artifacts/<name>.json. A missing file raises FileNotFoundError with
        a "run <name> first"-style message, matching every notebook's
        existing Section 1 behavior.

    Returns
    -------
    (config, summaries) -- `config` is a PlatformConfig; `summaries` is a
    dict keyed by the names passed in `required_summaries`.
    """
    project_root = Path(project_root)
    artifacts_dir = project_root / "artifacts"
    config_path = artifacts_dir / "project_config.json"

    if not config_path.exists():
        raise FileNotFoundError(
            f"{config_path} not found.\nFix: run 01_business_understanding.ipynb first."
        )
    with open(config_path, "r", encoding="utf-8") as f:
        raw_config = json.load(f)

    summaries: Dict[str, Dict[str, Any]] = {}
    for name in required_summaries or ():
        summary_path = artifacts_dir / f"{name}.json"
        if not summary_path.exists():
            raise FileNotFoundError(
                f"{summary_path} not found.\nFix: run the notebook that produces "
                f"'{name}' first."
            )
        with open(summary_path, "r", encoding="utf-8") as f:
            summaries[name] = json.load(f)

    return PlatformConfig(raw_config, project_root, artifacts_dir), summaries
