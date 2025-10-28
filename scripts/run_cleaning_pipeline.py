"""运行数据清洗流水线，生成 processed CSV 与 integrated_data.csv"""

import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def clean_meta() -> pd.DataFrame:
    meta_file = RAW_DIR / "meta_ads_raw.csv"
    df = pd.read_csv(meta_file, na_values=["--"])

    rename_dict = {
        "Reporting starts": "date",
        "Reporting ends": "date_end",
        "Campaign name": "campaign_name",
        "Amount spent (USD)": "spend",
        "Impressions": "impressions",
        "Link clicks": "clicks",
        "Purchases": "conversions",
        "Cost per purchase (USD)": "cpa_meta",
        "Purchase conversion value (USD)": "revenue",
        "Reach": "reach",
    }
    df = df.rename(columns=rename_dict)
    df.drop(columns=["date_end"], inplace=True)

    df["date"] = pd.to_datetime(df["date"])

    # 数值转换
    numeric_cols = ["spend", "impressions", "clicks", "conversions", "revenue", "cpa_meta"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["platform"] = "Meta"
    df["has_conversion_tracking"] = df["conversions"].notna()

    df["ctr"] = df["clicks"] / df["impressions"]
    df["cvr"] = df["conversions"] / df["clicks"]
    df["cpa"] = df["spend"] / df["conversions"]
    df["roas"] = df["revenue"] / df["spend"]

    for col in ["ctr", "cvr", "cpa", "roas"]:
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)

    df = df.sort_values(["campaign_name", "date"]).reset_index(drop=True)

    final_columns = [
        "date",
        "platform",
        "campaign_name",
        "spend",
        "impressions",
        "clicks",
        "conversions",
        "revenue",
        "ctr",
        "cvr",
        "cpa",
        "roas",
        "has_conversion_tracking",
        "reach",
    ]

    df_final = df[final_columns]
    df_final.to_csv(PROCESSED_DIR / "meta_cleaned.csv", index=False)
    return df_final


def clean_google() -> pd.DataFrame:
    google_file = RAW_DIR / "google_ads_raw.csv"
    column_names = [
        "date",
        "campaign_name",
        "campaign_id",
        "impressions",
        "clicks",
        "spend_google",
        "conversions",
        "cvr_google",
        "cpa_google",
        "revenue",
    ]

    df = pd.read_csv(google_file, skiprows=4, names=column_names, na_values=["--"])

    df["date"] = pd.to_datetime(df["date"])
    df["impressions"] = pd.to_numeric(df["impressions"], errors="coerce")
    df["clicks"] = pd.to_numeric(df["clicks"], errors="coerce")
    df["spend_google"] = pd.to_numeric(df["spend_google"], errors="coerce")

    df["conversions"] = df["conversions"].replace("< 10", "5").astype(float)
    df["cvr_google"] = (
        df["cvr_google"].str.replace("%", "", regex=False).astype(float) / 100
    )

    df.rename(
        columns={
            "spend_google": "spend",
            "cvr_google": "cvr",
            "cpa_google": "cpa_google_raw",
        },
        inplace=True,
    )

    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")

    df["ctr"] = df["clicks"] / df["impressions"]
    df["cvr"] = df["conversions"] / df["clicks"]
    df["cpa"] = df["spend"] / df["conversions"]
    df["roas"] = df["revenue"] / df["spend"]

    for col in ["ctr", "cvr", "cpa", "roas"]:
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)

    df["platform"] = "Google"

    final_columns = [
        "date",
        "platform",
        "campaign_name",
        "spend",
        "impressions",
        "clicks",
        "conversions",
        "revenue",
        "ctr",
        "cvr",
        "cpa",
        "roas",
    ]

    df_final = df[final_columns]
    df_final.to_csv(PROCESSED_DIR / "google_cleaned.csv", index=False)
    return df_final


def clean_tiktok() -> pd.DataFrame:
    tiktok_file = RAW_DIR / "tiktok_ads_raw.csv"
    df = pd.read_csv(tiktok_file, na_values=["--"])

    rename_map = {
        "Date": "date",
        "Campaign Name": "campaign_name",
        "Ad Group Name": "ad_group_name",
        "Cost": "spend",
        "Impressions": "impressions",
        "Clicks": "clicks",
        "Conversions": "conversions",
        "CPA": "cpa_raw",
        "CTR": "ctr_raw",
        "CVR": "cvr_raw",
        "Video Views": "video_views",
        "Video Play Actions": "video_actions",
        "Learning Status": "learning_status",
    }
    df = df.rename(columns=rename_map)
    df["date"] = pd.to_datetime(df["date"])

    numeric_cols = ["spend", "impressions", "clicks", "conversions", "video_views", "video_actions"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["ctr"] = df["ctr_raw"].str.replace("%", "", regex=False).astype(float) / 100
    df["cvr"] = df["cvr_raw"].str.replace("%", "", regex=False).astype(float) / 100
    df["revenue"] = df["conversions"] * 80
    df["cpa"] = df["spend"] / df["conversions"]
    df["roas"] = df["revenue"] / df["spend"]

    for col in ["ctr", "cvr", "cpa", "roas"]:
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)

    df["platform"] = "TikTok"
    df["is_learning"] = df["learning_status"].fillna("").str.contains("Learning")

    final_columns = [
        "date",
        "platform",
        "campaign_name",
        "spend",
        "impressions",
        "clicks",
        "conversions",
        "revenue",
        "ctr",
        "cvr",
        "cpa",
        "roas",
        "is_learning",
    ]

    df_final = df[final_columns]
    df_final.to_csv(PROCESSED_DIR / "tiktok_cleaned.csv", index=False)
    return df_final


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    meta_df = clean_meta()
    google_df = clean_google()
    tiktok_df = clean_tiktok()

    integrated = pd.concat([meta_df, google_df, tiktok_df], ignore_index=True)
    integrated.to_csv(PROCESSED_DIR / "integrated_data.csv", index=False)

    print(f"[OK] Integrated data saved: {len(integrated)} rows")


if __name__ == "__main__":
    main()
