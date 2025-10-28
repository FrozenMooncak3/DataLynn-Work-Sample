"""
Pipeline modules for the Datalynn project.
"""

from .week1_data_prep import (
    Week1Outputs,
    clean_google_ads,
    clean_meta_ads,
    clean_tiktok_ads,
    integrate_platforms,
    run_week1_pipeline,
)
from .week2_roas_modeling import (
    ModelArtifacts,
    prepare_daily_features,
    build_feature_matrix,
    run_week2_pipeline,
)
from .week3_ab_testing import (
    ABTestOutputs,
    run_week3_pipeline,
    simulate_dataset,
)

__all__ = [
    "Week1Outputs",
    "clean_google_ads",
    "clean_meta_ads",
    "clean_tiktok_ads",
    "integrate_platforms",
    "run_week1_pipeline",
    "ModelArtifacts",
    "prepare_daily_features",
    "build_feature_matrix",
    "run_week2_pipeline",
    "ABTestOutputs",
    "run_week3_pipeline",
    "simulate_dataset",
]

