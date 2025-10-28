#!/usr/bin/env python3
"""
一键运行 DataLynn 项目的三条核心流水线：
1. Week 1 数据清洗
2. Week 2 ROAS 建模
3. Week 3 创意 A/B 测试分析

使用方法
--------
python scripts/run_all_pipelines.py

该脚本只负责调度，方便一次性跑通；如需单独排查，可继续使用
`scripts/run_week{1,2,3}_pipeline.py`。
"""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.pipelines.week1_data_prep import run_week1_pipeline  # noqa: E402
from src.pipelines.week2_roas_modeling import run_week2_pipeline  # noqa: E402
from src.pipelines.week3_ab_testing import (  # noqa: E402
    run_week3_pipeline,
    simulate_dataset,
)


def run_week1() -> None:
    raw_dir = PROJECT_ROOT / "data" / "raw"
    processed_dir = PROJECT_ROOT / "data" / "processed"
    outputs = run_week1_pipeline(raw_dir=raw_dir, processed_dir=processed_dir)
    print("\n✅ Week 1 完成：")
    print(f"   Meta cleaned    → {outputs.meta_cleaned}")
    print(f"   Google cleaned  → {outputs.google_cleaned}")
    print(f"   TikTok cleaned  → {outputs.tiktok_cleaned}")
    print(f"   Integrated data → {outputs.integrated}")


def run_week2() -> None:
    integrated_path = PROJECT_ROOT / "data" / "processed" / "integrated_data.csv"
    models_dir = PROJECT_ROOT / "output" / "models"
    reports_dir = PROJECT_ROOT / "output" / "reports"
    artifacts = run_week2_pipeline(
        integrated_path=integrated_path,
        models_dir=models_dir,
        metrics_dir=reports_dir,
    )
    print("\n✅ Week 2 完成：")
    print(f"   Model saved   → {artifacts.model_path}")
    print(f"   Metrics saved → {artifacts.metrics_path}")


def run_week3() -> None:
    data_dir = PROJECT_ROOT / "data" / "ab_test"
    figures_dir = PROJECT_ROOT / "output" / "figures"
    reports_dir = PROJECT_ROOT / "output" / "reports"

    creative_a = data_dir / "creative_a.csv"
    creative_b = data_dir / "creative_b.csv"
    if not creative_a.exists() or not creative_b.exists():
        print("   未找到 A/B 测试原始 CSV，自动生成模拟数据...")
        simulate_dataset(data_dir)

    outputs = run_week3_pipeline(
        data_dir=data_dir,
        figures_dir=figures_dir,
        reports_dir=reports_dir,
    )
    print("\n✅ Week 3 完成：")
    print(f"   Summary CSV   → {outputs.summary_csv}")
    print(f"   t-test CSV    → {outputs.ttest_csv}")
    print(f"   Trend figure  → {outputs.figure_trend}")
    print(f"   Boxplot figure→ {outputs.figure_boxplot}")
    print(f"   Report MD     → {outputs.report_md}")


def main() -> None:
    print("🚀 正在运行 DataLynn 全流程流水线...")
    run_week1()
    run_week2()
    run_week3()
    print("\n🎉 全部流水线执行完成，可以继续检查输出或推送仓库。")


if __name__ == "__main__":
    main()
