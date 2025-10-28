#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TikTok Ads 数据清洗模块

用途：清洗 TikTok Ads 原始数据，统一格式和字段名
标准：必须与 Meta 清洗方法保持一致（参考 meta_cleaner.py）

重要：
- 本文件是模板，等待用户完成数据清洗任务后填充
- 清洗前必须读取 meta_cleaner.py 确认 baseline 标准
- 清洗后必须运行 scripts/check_consistency.py 验证一致性
"""

import pandas as pd
import numpy as np
from pathlib import Path

# 定义项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def clean_tiktok_ads(file_path: str) -> pd.DataFrame:
    """
    清洗 TikTok Ads 原始数据

    Args:
        file_path (str): TikTok Ads 原始 CSV 文件路径

    Returns:
        pd.DataFrame: 清洗后的数据

    清洗步骤（必须与 Meta baseline 保持一致）：
    1. 读取数据（encoding='utf-8-sig' 处理 BOM 问题）
    2. 处理缺失值（⚠️ 使用 na_values=['--']，与 Meta 一致）
    3. 处理 Learning 状态标记
    4. 处理百分比字符串（如果有）
    5. 统一列名（与 Meta 保持一致）
    6. 计算字段（CTR, CVR, CPA, ROAS，公式与 Meta 一致）
    7. 处理除零错误（.replace([np.inf, -np.inf], np.nan)）
    8. 添加 platform 列和 is_learning 列
    9. 选择最终列（顺序与 Meta 一致）
    """

    # ==================== Step 1: 读取原始数据 ====================
    # TODO: 用户填充
    # 提示：
    # - encoding='utf-8-sig'（处理 UTF-8 BOM 问题）
    # - na_values=['--'] ⚠️ 关键！与 Meta 保持一致

    print("🔄 Step 1: 读取 TikTok Ads 原始数据...")
    # df_tiktok = pd.read_csv(file_path, encoding='utf-8-sig', na_values=['--'])

    # ==================== Step 2: 处理 Learning 状态 ====================
    # TODO: 用户填充
    # 提示：
    # - 添加 is_learning 列标记（True/False）
    # - ⚠️ 不删除 Learning 状态的数据，只标记

    print("🔄 Step 2: 处理 Learning 状态...")

    # ==================== Step 3: 处理百分比字符串 ====================
    # TODO: 用户填充
    # 提示：如果 TikTok 有百分比字符串，需要转换

    print("🔄 Step 3: 处理百分比字符串（如果有）...")

    # ==================== Step 4: 统一列名 ====================
    # TODO: 用户填充
    # 提示：重命名列，使字段名与 Meta 一致
    # 必须包含：date, platform, campaign_name, spend, impressions,
    #          clicks, conversions, revenue, ctr, cvr, cpa, roas

    print("🔄 Step 4: 统一列名...")

    # ==================== Step 5: 计算字段 ====================
    # TODO: 用户填充
    # 提示：
    # - TikTok 需要自己计算所有指标（CTR, CVR, CPA, ROAS）
    # - ⚠️ 公式必须与 Meta 一致！
    # - ctr = clicks / impressions
    # - cvr = conversions / clicks
    # - cpa = spend / conversions
    # - roas = revenue / spend

    print("🔄 Step 5: 计算 CTR, CVR, CPA, ROAS...")

    # df_tiktok['ctr'] = df_tiktok['clicks'] / df_tiktok['impressions']
    # df_tiktok['cvr'] = df_tiktok['conversions'] / df_tiktok['clicks']
    # df_tiktok['cpa'] = df_tiktok['spend'] / df_tiktok['conversions']
    # df_tiktok['roas'] = df_tiktok['revenue'] / df_tiktok['spend']

    # ==================== Step 6: 处理除零错误 ====================
    # TODO: 用户填充
    # 提示：.replace([np.inf, -np.inf], np.nan)

    print("🔄 Step 6: 处理除零错误...")

    # df_tiktok['ctr'] = df_tiktok['ctr'].replace([np.inf, -np.inf], np.nan)
    # df_tiktok['cvr'] = df_tiktok['cvr'].replace([np.inf, -np.inf], np.nan)
    # df_tiktok['cpa'] = df_tiktok['cpa'].replace([np.inf, -np.inf], np.nan)
    # df_tiktok['roas'] = df_tiktok['roas'].replace([np.inf, -np.inf], np.nan)

    # ==================== Step 7: 添加 platform 列 ====================
    # TODO: 用户填充

    print("🔄 Step 7: 添加 platform 列...")

    # ==================== Step 8: 选择最终列 ====================
    # TODO: 用户填充
    # 提示：
    # - 列顺序必须与 Meta 一致
    # - TikTok 特有字段：is_learning

    print("🔄 Step 8: 选择最终列...")

    # final_columns = [
    #     'date',
    #     'platform',
    #     'campaign_name',
    #     'spend',
    #     'impressions',
    #     'clicks',
    #     'conversions',
    #     'revenue',
    #     'ctr',
    #     'cvr',
    #     'cpa',
    #     'roas',
    #     'is_learning'  # TikTok-specific field
    # ]
    # df_tiktok = df_tiktok[final_columns]

    print("✅ TikTok Ads 数据清洗完成！")
    # return df_tiktok

    # 临时返回空 DataFrame（用户完成后删除）
    return pd.DataFrame()


def main():
    """主函数：加载原始数据，清洗，保存"""

    # 原始数据路径
    raw_file = PROJECT_ROOT / "data/raw/tiktok_ads_raw.csv"

    # 清洗数据
    df_cleaned = clean_tiktok_ads(raw_file)

    # 保存清洗后的数据
    output_file = PROJECT_ROOT / "data/processed/tiktok_cleaned.csv"
    df_cleaned.to_csv(output_file, index=False)
    print(f"✅ 清洗后的数据已保存到: {output_file}")

    # 打印数据概览
    print("\n" + "=" * 50)
    print("数据概览")
    print("=" * 50)
    print(f"总行数: {len(df_cleaned)}")
    print(f"\n前5行:")
    print(df_cleaned.head())
    print(f"\n字段列表:")
    print(df_cleaned.columns.tolist())


if __name__ == "__main__":
    main()
