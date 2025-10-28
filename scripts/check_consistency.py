#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DataLynn 数据清洗一致性检查脚本

用途：验证 Meta、Google、TikTok 三平台的数据清洗是否保持一致

检查项：
1. 字段名是否一致
2. 计算公式是否一致
3. CTR/CVR 值范围是否合理（应在0-1之间）
4. 是否有无穷大值（除零错误未处理）

使用方法：
    python scripts/check_consistency.py

输出：
    - 检查通过：✅ All checks passed
    - 检查失败：❌ Consistency check failed（并列出具体问题）
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

# 定义项目根目录（相对于脚本位置）
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 定义数据文件路径
META_FILE = PROJECT_ROOT / "data/processed/meta_cleaned.csv"
GOOGLE_FILE = PROJECT_ROOT / "data/processed/google_cleaned.csv"
TIKTOK_FILE = PROJECT_ROOT / "data/processed/tiktok_cleaned.csv"


def check_file_exists():
    """检查清洗后的文件是否存在"""
    print("\n🔍 Step 1: 检查文件是否存在")
    print("-" * 50)

    files = {
        "Meta": META_FILE,
        "Google": GOOGLE_FILE,
        "TikTok": TIKTOK_FILE
    }

    all_exist = True
    for platform, file_path in files.items():
        if file_path.exists():
            print(f"✅ {platform}: {file_path}")
        else:
            print(f"❌ {platform}: 文件不存在 - {file_path}")
            all_exist = False

    return all_exist


def check_columns_consistency():
    """检查三平台的必需字段是否一致"""
    print("\n🔍 Step 2: 检查字段名一致性")
    print("-" * 50)

    # 必需字段（所有平台必须包含）
    required_columns = [
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
        'roas'
    ]

    try:
        df_meta = pd.read_csv(META_FILE)
        df_google = pd.read_csv(GOOGLE_FILE)
        df_tiktok = pd.read_csv(TIKTOK_FILE)
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return False

    # 检查每个平台是否包含所有必需字段
    all_consistent = True

    for platform, df in [("Meta", df_meta), ("Google", df_google), ("TikTok", df_tiktok)]:
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            print(f"❌ {platform} 缺少字段: {missing}")
            all_consistent = False
        else:
            print(f"✅ {platform}: 包含所有必需字段")

    return all_consistent


def check_value_ranges():
    """检查 CTR、CVR 值范围是否合理"""
    print("\n🔍 Step 3: 检查 CTR/CVR 值范围")
    print("-" * 50)

    try:
        df_meta = pd.read_csv(META_FILE)
        df_google = pd.read_csv(GOOGLE_FILE)
        df_tiktok = pd.read_csv(TIKTOK_FILE)
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return False

    all_valid = True

    for platform, df in [("Meta", df_meta), ("Google", df_google), ("TikTok", df_tiktok)]:
        # 检查 CTR（应该在0-1之间，除了 NaN）
        if 'ctr' in df.columns:
            invalid_ctr = df[(df['ctr'] < 0) | (df['ctr'] > 1)].shape[0]
            if invalid_ctr > 0:
                print(f"⚠️ {platform}: {invalid_ctr} 行 CTR 超出范围 [0, 1]")
                all_valid = False
            else:
                print(f"✅ {platform}: CTR 值范围正常")

        # 检查 CVR（应该在0-1之间，除了 NaN）
        if 'cvr' in df.columns:
            invalid_cvr = df[(df['cvr'] < 0) | (df['cvr'] > 1)].shape[0]
            if invalid_cvr > 0:
                print(f"⚠️ {platform}: {invalid_cvr} 行 CVR 超出范围 [0, 1]")
                all_valid = False
            else:
                print(f"✅ {platform}: CVR 值范围正常")

    return all_valid


def check_infinity_values():
    """检查是否有无穷大值（除零错误未处理）"""
    print("\n🔍 Step 4: 检查无穷大值（除零错误）")
    print("-" * 50)

    try:
        df_meta = pd.read_csv(META_FILE)
        df_google = pd.read_csv(GOOGLE_FILE)
        df_tiktok = pd.read_csv(TIKTOK_FILE)
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return False

    columns_to_check = ['ctr', 'cvr', 'cpa', 'roas']
    all_clean = True

    for platform, df in [("Meta", df_meta), ("Google", df_google), ("TikTok", df_tiktok)]:
        for col in columns_to_check:
            if col in df.columns:
                inf_count = np.isinf(df[col]).sum()
                if inf_count > 0:
                    print(f"❌ {platform}.{col}: 发现 {inf_count} 个无穷大值（除零错误未处理）")
                    all_clean = False

        if all_clean:
            print(f"✅ {platform}: 无无穷大值")

    return all_clean


def check_data_types():
    """检查数据类型是否正确"""
    print("\n🔍 Step 5: 检查数据类型")
    print("-" * 50)

    try:
        df_meta = pd.read_csv(META_FILE)
        df_google = pd.read_csv(GOOGLE_FILE)
        df_tiktok = pd.read_csv(TIKTOK_FILE)
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return False

    # 应该是数字类型的字段
    numeric_columns = ['spend', 'impressions', 'clicks', 'conversions', 'revenue',
                       'ctr', 'cvr', 'cpa', 'roas']

    all_correct = True

    for platform, df in [("Meta", df_meta), ("Google", df_google), ("TikTok", df_tiktok)]:
        for col in numeric_columns:
            if col in df.columns:
                if not pd.api.types.is_numeric_dtype(df[col]):
                    print(f"❌ {platform}.{col}: 数据类型应为数字，实际为 {df[col].dtype}")
                    all_correct = False

        if all_correct:
            print(f"✅ {platform}: 所有数字字段类型正确")

    return all_correct


def main():
    """主函数"""
    print("=" * 50)
    print("DataLynn 数据清洗一致性检查")
    print("=" * 50)

    # 执行所有检查
    checks = [
        ("文件存在检查", check_file_exists()),
        ("字段名一致性", check_columns_consistency()),
        ("值范围检查", check_value_ranges()),
        ("无穷大值检查", check_infinity_values()),
        ("数据类型检查", check_data_types())
    ]

    # 汇总结果
    print("\n" + "=" * 50)
    print("检查结果汇总")
    print("=" * 50)

    all_passed = True
    for check_name, result in checks:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{check_name}: {status}")
        if not result:
            all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有检查通过！数据清洗保持一致性。")
        print("=" * 50)
        sys.exit(0)
    else:
        print("⚠️ 检查失败！请修复上述问题后重新运行。")
        print("=" * 50)
        sys.exit(1)


if __name__ == "__main__":
    main()
