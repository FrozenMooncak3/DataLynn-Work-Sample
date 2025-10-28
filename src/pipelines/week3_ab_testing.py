"""
Week 3 A/B testing pipeline.

Provides reusable helpers to:
1. simulate creative performance data (for demos or unit tests),
2. load/clean archival test results,
3. run Welch's t-test with effect sizes, and
4. generate summary tables, figures, and a Markdown report.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats


plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


@dataclass
class ABTestOutputs:
    summary_csv: Path
    ttest_csv: Path
    figure_trend: Path
    figure_boxplot: Path
    report_md: Path


def simulate_creative(
    name: str,
    num_days: int,
    spend_mean: float,
    spend_std: float,
    imp_mean: float,
    imp_std: float,
    ctr_mean: float,
    ctr_std: float,
    cvr_mean: float,
    cvr_std: float,
    learning_period: int,
    learning_penalty: float,
    avg_order_value: float = 86.0,
) -> pd.DataFrame:
    """Generate day-level metrics for a creative arm."""
    days = np.arange(1, num_days + 1)
    spend = np.random.normal(spend_mean, spend_std, num_days)
    spend = np.clip(spend, spend_mean * 0.75, spend_mean * 1.35)

    impressions = np.random.normal(imp_mean, imp_std, num_days)
    impressions = np.clip(impressions, imp_mean * 0.7, imp_mean * 1.4).astype(int)

    ctr = np.random.normal(ctr_mean, ctr_std, num_days)
    ctr = np.clip(ctr, 0.005, None)

    cvr = np.random.normal(cvr_mean, cvr_std, num_days)
    cvr = np.clip(cvr, 0.003, None)

    ctr[:learning_period] *= learning_penalty
    cvr[:learning_period] *= learning_penalty

    clicks = np.round(impressions * ctr).astype(int)
    clicks = np.clip(clicks, 1, None)

    conversions = np.round(clicks * cvr).astype(int)
    conversions = np.clip(conversions, 0, clicks)

    revenue = conversions * avg_order_value

    ctr_actual = clicks / impressions
    cvr_actual = np.divide(conversions, clicks, out=np.zeros_like(conversions, dtype=float), where=clicks > 0)
    cpa = np.divide(spend, conversions, out=np.full_like(spend, np.nan), where=conversions > 0)
    roas = np.divide(revenue, spend, out=np.zeros_like(revenue, dtype=float), where=spend > 0)

    return pd.DataFrame(
        {
            "creative": name,
            "day": days,
            "spend": np.round(spend, 2),
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "revenue": np.round(revenue, 2),
            "roas": roas,
            "cpa": cpa,
            "ctr": ctr_actual,
            "cvr": cvr_actual,
        }
    )


def simulate_dataset(
    output_dir: Path,
    random_seed: int = 20241012,
    learning_period: int = 7,
    num_days: int = 35,
) -> Dict[str, Path]:
    """Generate Creative A/B CSVs for demo purposes."""
    output_dir.mkdir(parents=True, exist_ok=True)
    np.random.seed(random_seed)

    creative_a = simulate_creative(
        name="A",
        num_days=num_days,
        spend_mean=1180,
        spend_std=110,
        imp_mean=88000,
        imp_std=9000,
        ctr_mean=0.026,
        ctr_std=0.0022,
        cvr_mean=0.031,
        cvr_std=0.0028,
        learning_period=learning_period,
        learning_penalty=0.82,
    )

    creative_b = simulate_creative(
        name="B",
        num_days=num_days,
        spend_mean=1195,
        spend_std=115,
        imp_mean=90500,
        imp_std=9500,
        ctr_mean=0.0285,
        ctr_std=0.0024,
        cvr_mean=0.0345,
        cvr_std=0.0030,
        learning_period=learning_period,
        learning_penalty=0.86,
    )

    path_a = output_dir / "creative_a.csv"
    path_b = output_dir / "creative_b.csv"
    creative_a.to_csv(path_a, index=False)
    creative_b.to_csv(path_b, index=False)

    return {"creative_a": path_a, "creative_b": path_b}


def load_creatives(data_dir: Path) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load creative A/B CSVs."""
    creative_a = pd.read_csv(data_dir / "creative_a.csv")
    creative_b = pd.read_csv(data_dir / "creative_b.csv")
    return creative_a, creative_b


def strip_learning_period(
    creative_a: pd.DataFrame,
    creative_b: pd.DataFrame,
    learning_period: int,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Exclude the learning period from both groups."""
    mask = lambda df: df[df["day"] > learning_period].copy()
    return mask(creative_a), mask(creative_b)


def summarise_metrics(
    creative_a: pd.DataFrame,
    creative_b: pd.DataFrame,
    metrics: Iterable[str] = ("roas", "cpa", "ctr", "cvr"),
) -> pd.DataFrame:
    """Compute mean/std summary for key metrics."""
    rows = []
    for metric in metrics:
        mean_a = creative_a[metric].mean()
        std_a = creative_a[metric].std()
        mean_b = creative_b[metric].mean()
        std_b = creative_b[metric].std()
        rows.append(
            {
                "Metric": metric.upper(),
                "Creative A (Mean)": round(mean_a, 4),
                "Creative A (Std)": round(std_a, 4),
                "Creative B (Mean)": round(mean_b, 4),
                "Creative B (Std)": round(std_b, 4),
                "Difference (B - A)": round(mean_b - mean_a, 4),
            }
        )
    return pd.DataFrame(rows)


def run_ttests(
    creative_a: pd.DataFrame,
    creative_b: pd.DataFrame,
    metrics: Iterable[str] = ("roas", "cpa", "ctr", "cvr"),
) -> pd.DataFrame:
    """Execute Welch's t-test and compute effect sizes."""
    rows = []
    for metric in metrics:
        a = creative_a[metric]
        b = creative_b[metric]
        t_stat, p_value = stats.ttest_ind(b, a, equal_var=False)
        mean_diff = b.mean() - a.mean()
        pooled_std = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
        cohens_d = mean_diff / pooled_std if pooled_std > 0 else np.nan
        rows.append(
            {
                "Metric": metric.upper(),
                "Creative A Mean": round(a.mean(), 4),
                "Creative B Mean": round(b.mean(), 4),
                "Difference (B - A)": round(mean_diff, 4),
                "t-statistic": round(t_stat, 4),
                "p-value": round(p_value, 4),
                "Significant (p<0.05)": "Yes" if p_value < 0.05 else "No",
                "Cohen's d": round(cohens_d, 4),
            }
        )
    return pd.DataFrame(rows)


def plot_trend(
    creative_a: pd.DataFrame,
    creative_b: pd.DataFrame,
    learning_period: int,
    output_dir: Path,
) -> Path:
    """Plot ROAS trend with learning period highlighted."""
    output_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(creative_a["day"], creative_a["roas"], marker="o", label="Creative A")
    ax.plot(creative_b["day"], creative_b["roas"], marker="o", label="Creative B")
    ax.axvspan(1, learning_period, color="gray", alpha=0.15, label="Learning period")
    ax.set_xlabel("Day")
    ax.set_ylabel("ROAS")
    ax.set_title("Daily ROAS trend (learning period shaded)")
    ax.legend()
    fig.tight_layout()
    path = output_dir / "ab_test_roas_trend.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)
    return path


def plot_distributions(
    creative_a: pd.DataFrame,
    creative_b: pd.DataFrame,
    output_dir: Path,
    metrics: Iterable[str] = ("roas", "cpa", "ctr", "cvr"),
) -> Path:
    """Create boxplots comparing distributions across creatives."""
    output_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    metric_titles = {"roas": "ROAS", "cpa": "CPA", "ctr": "CTR", "cvr": "CVR"}
    for idx, metric in enumerate(metrics):
        ax = axes[idx // 2, idx % 2]
        plot_df = pd.DataFrame(
            {
                metric: pd.concat(
                    [creative_a[metric], creative_b[metric]],
                    ignore_index=True,
                ),
                "Creative": ["A"] * len(creative_a) + ["B"] * len(creative_b),
            }
        )
        sns.boxplot(data=plot_df, x="Creative", y=metric, ax=ax)
        ax.set_title(f"{metric_titles[metric]} distribution")
        ax.set_xlabel("Creative")
        ax.set_ylabel(metric_titles[metric])
    fig.tight_layout()
    path = output_dir / "ab_test_comparison.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)
    return path


def build_report(
    summary_df: pd.DataFrame,
    ttest_df: pd.DataFrame,
    learning_period: int,
    stable_days: int,
    output_path: Path,
) -> Path:
    """Write a Markdown report summarising the test."""
    roas_row = ttest_df.loc[ttest_df["Metric"] == "ROAS"].iloc[0]
    is_significant = roas_row["p-value"] < 0.05 and roas_row["Difference (B - A)"] > 0
    lines = [
        "# A/B Test Report — Creative A vs Creative B",
        "",
        f"**Generated at**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Learning period**: first {learning_period} days excluded",
        f"**Stable window**: {stable_days} days per arm",
        "",
        "## Metric summary (stable period)",
        summary_df.to_markdown(index=False),
        "",
        "## t-test results",
        ttest_df.to_markdown(index=False),
        "",
        "## Recommendation",
        "🟢 **Promote Creative B**" if is_significant else "🔴 **Do not promote Creative B yet**",
        "",
        "### Rationale",
        (
            f"1. ROAS lift {roas_row['Difference (B - A)']:.4f} with p-value = {roas_row['p-value']:.4f}, "
            "clearing the significance bar."
            if is_significant
            else f"1. ROAS lift {roas_row['Difference (B - A)']:.4f} with p-value = {roas_row['p-value']:.4f}, "
            "not yet statistically significant."
        ),
        "2. CTR and CVR improvements signal a healthier funnel for Creative B.",
        "",
        "### Risks & next steps",
        "1. Monitor the more volatile CPA trend to avoid cost creep.",
        "2. Extend the test by 1–2 weeks to confirm the lift holds.",
    ]
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def run_week3_pipeline(
    data_dir: Path,
    figures_dir: Path,
    reports_dir: Path,
    learning_period: int = 7,
) -> ABTestOutputs:
    """Execute A/B test analysis end-to-end."""
    figures_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    creative_a, creative_b = load_creatives(data_dir)
    a_stable, b_stable = strip_learning_period(creative_a, creative_b, learning_period)
    summary = summarise_metrics(a_stable, b_stable)
    ttest = run_ttests(a_stable, b_stable)

    summary_path = reports_dir / "ab_test_summary.csv"
    ttest_path = reports_dir / "ab_test_ttest_results.csv"
    summary.to_csv(summary_path, index=False)
    ttest.to_csv(ttest_path, index=False)

    trend_path = plot_trend(creative_a, creative_b, learning_period, figures_dir)
    boxplot_path = plot_distributions(a_stable, b_stable, figures_dir)

    report_path = reports_dir / "ab_test_report.md"
    build_report(
        summary_df=summary,
        ttest_df=ttest,
        learning_period=learning_period,
        stable_days=len(a_stable),
        output_path=report_path,
    )

    return ABTestOutputs(
        summary_csv=summary_path,
        ttest_csv=ttest_path,
        figure_trend=trend_path,
        figure_boxplot=boxplot_path,
        report_md=report_path,
    )


__all__ = [
    "ABTestOutputs",
    "simulate_creative",
    "simulate_dataset",
    "load_creatives",
    "strip_learning_period",
    "summarise_metrics",
    "run_ttests",
    "plot_trend",
    "plot_distributions",
    "build_report",
    "run_week3_pipeline",
]
