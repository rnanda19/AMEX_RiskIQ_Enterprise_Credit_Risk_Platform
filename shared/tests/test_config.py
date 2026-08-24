import json

import pytest

from shared.config import load_platform_config


def _write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f)


def test_missing_project_config_raises_with_fix_hint(tmp_path):
    with pytest.raises(FileNotFoundError, match="01_business_understanding"):
        load_platform_config(tmp_path)


def test_loads_config_and_resolves_warp_thread_count(tmp_path):
    artifacts = tmp_path / "artifacts"
    _write_json(artifacts / "project_config.json", {
        "pillar_dirs": {"model_development": str(tmp_path / "model_dev")},
        "hardware": {"logical_cores_detected": 16},
        "random_seed": 42,
        "resource_limits": {"warp_thread_count": 15, "max_ram_bytes": 30_000_000_000},
    })
    config, summaries = load_platform_config(tmp_path)
    assert config.warp_thread_count == 15
    assert config.max_ram_bytes == 30_000_000_000
    assert config.random_seed == 42
    assert config.pillar_dir("model_development") == tmp_path / "model_dev"
    assert summaries == {}


def test_falls_back_to_detected_cores_on_older_config(tmp_path):
    """A config written before the resource_limits block existed should
    fall back to the raw detected core count, not crash."""
    artifacts = tmp_path / "artifacts"
    _write_json(artifacts / "project_config.json", {
        "pillar_dirs": {"data_engineering": str(tmp_path / "data_eng")},
        "hardware": {"logical_cores_detected": 8},
        "random_seed": 42,
    })
    config, _ = load_platform_config(tmp_path)
    assert config.warp_thread_count == 8
    assert config.max_ram_bytes is None


def test_required_summary_missing_raises(tmp_path):
    artifacts = tmp_path / "artifacts"
    _write_json(artifacts / "project_config.json", {
        "pillar_dirs": {}, "hardware": {"logical_cores_detected": 4}, "random_seed": 42,
    })
    with pytest.raises(FileNotFoundError, match="notebook_02_summary"):
        load_platform_config(tmp_path, required_summaries=["notebook_02_summary"])


def test_required_summary_loads_when_present(tmp_path):
    artifacts = tmp_path / "artifacts"
    _write_json(artifacts / "project_config.json", {
        "pillar_dirs": {}, "hardware": {"logical_cores_detected": 4}, "random_seed": 42,
    })
    _write_json(artifacts / "notebook_02_summary.json", {"output_files": {"x": "y"}})
    config, summaries = load_platform_config(tmp_path, required_summaries=["notebook_02_summary"])
    assert summaries["notebook_02_summary"]["output_files"]["x"] == "y"


def test_unknown_pillar_raises_keyerror_listing_available(tmp_path):
    artifacts = tmp_path / "artifacts"
    _write_json(artifacts / "project_config.json", {
        "pillar_dirs": {"data_engineering": str(tmp_path / "d")},
        "hardware": {"logical_cores_detected": 4}, "random_seed": 42,
    })
    config, _ = load_platform_config(tmp_path)
    with pytest.raises(KeyError, match="data_engineering"):
        config.pillar_dir("model_development")
