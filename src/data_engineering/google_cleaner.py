#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Google Ads 数据清洗模块

用途：清洗 Google Ads 原始数据，统一格式和字段名
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


def clean_google_ads(file_path: str) -> pd.DataFrame:
    """
    清洗 Google Ads 原始数据

    Args:
        file_path (str): Google Ads 原始 CSV 文件路径

    Returns:
        pd.DataFrame: 清洗后的数据

    清洗步骤（必须与 Meta baseline 保持一致）：
    1. 读取数据（skiprows=4，跳过 metadata）
    2. 处理缺失值（⚠️ 使用 na_values=['--']，与 Meta 一致）
    3. 处理特殊值（'< 10' → 5）
    4. 处理百分比字符串（'4.80%' → 0.048）
    5. 统一列名（与 Meta 保持一致）
    6. 计算字段（CTR, CVR, CPA, ROAS，公式与 Meta 一致）
    7. 处理除零错误（.replace([np.inf, -np.inf], np.nan)）
    8. 添加 platform 列
    9. 选择最终列（顺序与 Meta 一致）
    """

    # ==================== Step 1: 读取原始数据 ====================
    # TODO: 用户填充
    # 提示：
    # - skiprows=4（跳过前4行 metadata）
    # - names=[...] 自定义列名
    # - na_values=['--'] ⚠️ 关键！与 Meta 保持一致

    print("🔄 Step 1: 读取 Google Ads 原始数据...")
    # df_google = pd.read_csv(file_path, ...)

    # ==================== Step 2: 处理特殊值 ====================
    # TODO: 用户填充
    # 提示：处理 '< 10' 隐私保护值

    print("🔄 Step 2: 处理特殊值 '< 10'...")

    # ==================== Step 3: 处理百分比字符串 ====================
    # TODO: 用户填充
    # 提示：'4.80%' → 0.048

    print("🔄 Step 3: 处理百分比字符串...")

    # ==================== Step 4: 统一列名 ====================
    # TODO: 用户填充
    # 提示：重命名列，使字段名与 Meta 一致
    # 必须包含：date, platform, campaign_name, spend, impressions,
    #          clicks, conversions, revenue, ctr, cvr, cpa, roas

    print("🔄 Step 4: 统一列名...")

    # ==================== Step 5: 计算字段 ====================
    # TODO: 用户填充
    # 提示：
    # - Google 已经提供了 CTR, CVR, CPA（可能需要转换）
    # - 需要自己计算 ROAS = revenue / spend
    # - ⚠️ 公式必须与 Meta 一致！

    print("🔄 Step 5: 计算 ROAS...")

    # ==================== Step 6: 处理除零错误 ====================
    # TODO: 用户填充
    # 提示：.replace([np.inf, -np.inf], np.nan)

    print("🔄 Step 6: 处理除零错误...")

    # ==================== Step 7: 添加 platform 列 ====================
    # TODO: 用户填充

    print("🔄 Step 7: 添加 platform 列...")

    # ==================== Step 8: 选择最终列 ====================
    # TODO: 用户填充
    # 提示：列顺序必须与 Meta 一致

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
    #     'roas'
    # ]
    # df_google = df_google[final_columns]

    print("✅ Google Ads 数据清洗完成！")
    # return df_google

    # 临时返回空 DataFrame（用户完成后删除）
    return pd.DataFrame()


def main():
    """主函数：加载原始数据，清洗，保存"""

    # 原始数据路径
    raw_file = PROJECT_ROOT / "data/raw/google_ads_raw.csv"

    # 清洗数据
    df_cleaned = clean_google_ads(raw_file)

    # 保存清洗后的数据
    output_file = PROJECT_ROOT / "data/processed/google_cleaned.csv"
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
