#!/usr/bin/env python3
"""
Run the Week 1 data preparation pipeline end-to-end.

Usage
-----
python scripts/run_week1_pipeline.py
"""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.pipelines.week1_data_prep import run_week1_pipeline  # noqa: E402


def main() -> None:
    raw_dir = PROJECT_ROOT / "data" / "raw"
    processed_dir = PROJECT_ROOT / "data" / "processed"
    outputs = run_week1_pipeline(raw_dir=raw_dir, processed_dir=processed_dir)
    print("Week1 pipeline completed.")
    print(f"Meta cleaned:     {outputs.meta_cleaned}")
    print(f"Google cleaned:   {outputs.google_cleaned}")
    print(f"TikTok cleaned:   {outputs.tiktok_cleaned}")
    print(f"Integrated data:  {outputs.integrated}")


if __name__ == "__main__":
    main()

