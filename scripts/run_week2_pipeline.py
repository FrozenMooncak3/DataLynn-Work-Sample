#!/usr/bin/env python3
"""
Train the Week 2 ROAS prediction model and persist artifacts.

Usage
-----
python scripts/run_week2_pipeline.py
"""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.pipelines.week2_roas_modeling import run_week2_pipeline  # noqa: E402


def main() -> None:
    integrated_path = PROJECT_ROOT / "data" / "processed" / "integrated_data.csv"
    models_dir = PROJECT_ROOT / "output" / "models"
    metrics_dir = PROJECT_ROOT / "output" / "reports"

    artifacts = run_week2_pipeline(
        integrated_path=integrated_path,
        models_dir=models_dir,
        metrics_dir=metrics_dir,
    )
    print("Week2 modeling pipeline completed.")
    print(f"Model saved to:   {artifacts.model_path}")
    print(f"Metrics saved to: {artifacts.metrics_path}")


if __name__ == "__main__":
    main()

