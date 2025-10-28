# -*- coding: utf-8 -*-
"""
Meta Ads Data Cleaning Module

Cleans Meta (Facebook/Instagram) ads data
Issues handled:
1. Column names with spaces and parentheses
2. "--" missing values
3. Brand_Awareness campaign has no conversion tracking
4. Decimal precision issues
5. Duplicate date columns
"""

import pandas as pd
import numpy as np


def clean_meta_data(file_path: str) -> pd.DataFrame:
    """
    Clean Meta Ads raw data

    Args:
        file_path: Path to Meta raw CSV file

    Returns:
        Cleaned DataFrame
    """

    # Step 1: Read data, specify "--" as missing value
    print("Reading Meta Ads data...")
    df = pd.read_csv(file_path, na_values=['--'])

    print(f"   Raw data: {len(df)} rows x {len(df.columns)} columns")

    # Step 2: Rename columns (remove spaces and parentheses)
    print("Renaming columns...")
    rename_dict = {
        'Reporting starts': 'date',
        'Reporting ends': 'date_end',  # Will be deleted later
        'Campaign name': 'campaign_name',
        'Amount spent (USD)': 'spend',
        'Impressions': 'impressions',
        'Link clicks': 'clicks',
        'Purchases': 'conversions',
        'Cost per purchase (USD)': 'cpa_meta',  # Meta-calculated CPA
        'Purchase conversion value (USD)': 'revenue',
        'Reach': 'reach'
    }
    df.rename(columns=rename_dict, inplace=True)

    # Step 3: Delete redundant date_end column (same as date)
    print("Deleting redundant column (date_end)...")
    df.drop(columns=['date_end'], inplace=True)

    # Step 4: Convert date format
    print("Converting date format...")
    df['date'] = pd.to_datetime(df['date'])

    # Step 5: Round money to 2 decimal places
    print("Rounding money to 2 decimal places...")
    money_columns = ['spend', 'cpa_meta', 'revenue']
    for col in money_columns:
        df[col] = df[col].round(2)

    # Step 6: Add conversion tracking flag
    print("Adding conversion tracking flag...")
    df['has_conversion_tracking'] = df['conversions'].notna()

    # Count rows without conversion tracking
    no_tracking = (~df['has_conversion_tracking']).sum()
    if no_tracking > 0:
        print(f"   Warning: {no_tracking} rows without conversion tracking (Brand_Awareness)")

    # Step 7: Add platform column
    print("Adding platform identifier...")
    df['platform'] = 'Meta'

    # Step 8: Calculate CTR and CVR
    print("Calculating CTR and CVR...")
    df['ctr'] = df['clicks'] / df['impressions']
    df['cvr'] = df['conversions'] / df['clicks']

    # Handle division by zero (replace with NaN)
    df['ctr'] = df['ctr'].replace([np.inf, -np.inf], np.nan)
    df['cvr'] = df['cvr'].replace([np.inf, -np.inf], np.nan)

    # Step 9: Calculate CPA (our own calculation)
    print("Calculating CPA and ROAS...")
    df['cpa'] = df['spend'] / df['conversions']
    df['cpa'] = df['cpa'].replace([np.inf, -np.inf], np.nan)

    # Step 10: Calculate ROAS
    df['roas'] = df['revenue'] / df['spend']
    df['roas'] = df['roas'].replace([np.inf, -np.inf], np.nan)

    # Step 11: Sort by date
    df.sort_values('date', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Step 12: Select final columns (standardized order)
    final_columns = [
        'date',
        'platform',
        'campaign_name',
        'spend',
        'impressions',
        'clicks',
        'conversions',
        'revenue',
        'ctr',
        'cvr',
        'cpa',
        'roas',
        'has_conversion_tracking',
        'reach'  # Meta-specific field
    ]

    df = df[final_columns]

    print(f"Meta data cleaning complete: {len(df)} rows x {len(df.columns)} columns")
    print()

    return df


def categorize_meta_campaign(campaign_name: str) -> str:
    """
    Categorize campaign by name

    Args:
        campaign_name: Campaign name

    Returns:
        Campaign type: 'brand_awareness' / 'prospecting' / 'retargeting' / 'test'
    """
    name_lower = campaign_name.lower()

    if 'brand' in name_lower or 'awareness' in name_lower:
        return 'brand_awareness'
    elif 'retargeting' in name_lower or 'retarget' in name_lower:
        return 'retargeting'
    elif 'test' in name_lower:
        return 'test'
    else:
        return 'prospecting'


if __name__ == '__main__':
    # Test code
    import os

    # Set paths
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    meta_file = os.path.join(project_root, 'data', 'raw', 'meta_ads_raw.csv')

    # Clean data
    df_clean = clean_meta_data(meta_file)

    # Display first 5 rows
    print("First 5 rows:")
    print(df_clean.head())
    print()

    # Display data info
    print("Data info:")
    print(df_clean.info())
    print()

    # Display missing values
    print("Missing values:")
    print(df_clean.isnull().sum())
