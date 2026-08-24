"""Tests monitoring_job.py the same way it's actually invoked in
production: as a CLI subprocess, with real (small, synthetic) CSVs and
JSON config on disk -- not by importing internals, since its whole
contract is the CLI + exit code (0 = OK/WATCH, 1 = ALERT), as documented
in its own header comment.
"""
import csv
import json
import subprocess
import sys
from pathlib import Path

MONITORING_JOB = (
    Path(__file__).resolve().parents[1] / "src" / "monitoring" / "monitoring_job.py"
)


def _run(new_data_csv, baseline_json, config_json, out_log):
    return subprocess.run(
        [
            sys.executable, str(MONITORING_JOB),
            "--new-data-csv", str(new_data_csv),
            "--baseline-json", str(baseline_json),
            "--config-json", str(config_json),
            "--out-log", str(out_log),
        ],
        capture_output=True, text=True,
    )


def _write_baseline_and_config(tmp_path, default_rate=0.2589, swing_threshold_pp=5.0):
    baseline = {
        "train_default_rate": default_rate,
        "psi_top_n_features": ["balance"],
        "quantile_bin_edges": {"balance": [0.0, 0.25, 0.5, 0.75, 1.0]},
    }
    config = {"thresholds": {"default_rate_swing_pp": swing_threshold_pp}}
    baseline_path = tmp_path / "monitoring_baseline.json"
    config_path = tmp_path / "monitoring_config.json"
    baseline_path.write_text(json.dumps(baseline))
    config_path.write_text(json.dumps(config))
    return baseline_path, config_path


def test_exits_zero_when_default_rate_within_threshold(tmp_path):
    baseline_path, config_path = _write_baseline_and_config(tmp_path, default_rate=0.2589, swing_threshold_pp=5.0)
    data_path = tmp_path / "new_batch.csv"
    with open(data_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["balance", "target"])
        # 26% observed default rate -- within 5pp of the 25.89% baseline.
        for i in range(100):
            writer.writerow([0.1 * (i % 10), 1 if i < 26 else 0])
    out_log = tmp_path / "log.csv"

    result = _run(data_path, baseline_path, config_path, out_log)
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    check = next(c for c in payload["checks"] if c["metric"] == "default_rate_swing_pp")
    assert check["status"] == "OK"
    assert out_log.exists()


def test_exits_one_when_default_rate_swings_past_threshold(tmp_path):
    baseline_path, config_path = _write_baseline_and_config(tmp_path, default_rate=0.2589, swing_threshold_pp=5.0)
    data_path = tmp_path / "new_batch.csv"
    with open(data_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["balance", "target"])
        # 60% observed default rate -- a huge swing past the 5pp threshold.
        for i in range(100):
            writer.writerow([0.1 * (i % 10), 1 if i < 60 else 0])
    out_log = tmp_path / "log.csv"

    result = _run(data_path, baseline_path, config_path, out_log)
    assert result.returncode == 1, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    check = next(c for c in payload["checks"] if c["metric"] == "default_rate_swing_pp")
    assert check["status"] == "ALERT"


def test_no_target_column_reports_not_computable_not_a_crash(tmp_path):
    """Unlabeled/not-yet-realized outcomes (no 'target' column) is a real,
    expected production scenario -- must report NOT_COMPUTABLE, not crash."""
    baseline_path, config_path = _write_baseline_and_config(tmp_path)
    data_path = tmp_path / "new_batch.csv"
    with open(data_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["balance"])
        for i in range(20):
            writer.writerow([0.1 * (i % 10)])
    out_log = tmp_path / "log.csv"

    result = _run(data_path, baseline_path, config_path, out_log)
    payload = json.loads(result.stdout)
    check = next(c for c in payload["checks"] if c["metric"] == "default_rate_swing_pp")
    assert check["status"] == "NOT_COMPUTABLE"
    assert result.returncode == 0  # not computable != alert


def test_appends_to_existing_log_without_duplicating_header(tmp_path):
    baseline_path, config_path = _write_baseline_and_config(tmp_path)
    data_path = tmp_path / "new_batch.csv"
    with open(data_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["balance"])
        writer.writerow([0.5])
    out_log = tmp_path / "log.csv"

    _run(data_path, baseline_path, config_path, out_log)
    _run(data_path, baseline_path, config_path, out_log)

    with open(out_log) as f:
        rows = list(csv.reader(f))
    assert rows[0] == ["run_at_utc", "new_data_csv", "n_rows", "any_alert"]
    assert len(rows) == 3  # header + 2 runs, no repeated header
