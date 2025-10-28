#!/usr/bin/env python3
"""
Execute the Week 3 A/B testing analysis pipeline.

The script optionally generates synthetic creative data if the CSVs are missing,
then runs the statistical analysis and writes out figures/reports.
"""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.pipelines.week3_ab_testing import (  # noqa: E402
    ABTestOutputs,
    run_week3_pipeline,
    simulate_dataset,
)


def ensure_data_exists(data_dir: Path) -> None:
    if not (data_dir / "creative_a.csv").exists() or not (data_dir / "creative_b.csv").exists():
        print("Creative CSVs not found. Generating simulated dataset...")
        simulate_dataset(data_dir)


def main() -> None:
    data_dir = PROJECT_ROOT / "data" / "ab_test"
    figures_dir = PROJECT_ROOT / "output" / "figures"
    reports_dir = PROJECT_ROOT / "output" / "reports"

    ensure_data_exists(data_dir)
    outputs: ABTestOutputs = run_week3_pipeline(
        data_dir=data_dir,
        figures_dir=figures_dir,
        reports_dir=reports_dir,
    )
    print("Week3 A/B testing pipeline completed.")
    print(f"Summary CSV:      {outputs.summary_csv}")
    print(f"t-test CSV:       {outputs.ttest_csv}")
    print(f"Trend figure:     {outputs.figure_trend}")
    print(f"Boxplot figure:   {outputs.figure_boxplot}")
    print(f"Report Markdown:  {outputs.report_md}")


if __name__ == "__main__":
    main()

