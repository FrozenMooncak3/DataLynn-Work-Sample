"""
生成真实格式的广告平台原始数据
模拟 Meta、Google、TikTok 三个平台全年（2024 年）的导出格式
预埋真实数据问题：季节性波动、节日峰值、缺失值、隐私脱敏、重复导出等
"""

import pandas as pd
import numpy as np
from datetime import datetime
import random


# 设置随机种子，保证可复现
np.random.seed(42)
random.seed(42)


# ==================== 全年时间范围与季节性设置 ====================
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 12, 31)
DATE_RANGE = pd.date_range(START_DATE, END_DATE, freq="D")

# 月度基准（基于真实投放节奏的经验值）
MONTH_SPEND_MULTIPLIER = {
    1: 0.95,  # 新年放缓
    2: 1.05,  # 情人节促销
    3: 1.00,
    4: 0.95,
    5: 1.00,
    6: 0.93,  # 初夏投放略降
    7: 0.92,
    8: 1.05,  # 返校季预热
    9: 1.08,
    10: 1.15,  # Q4 逐渐升温
    11: 1.35,  # 黑五
    12: 1.40,  # 假日旺季
}

MONTH_CTR_MULTIPLIER = {
    1: 0.98,
    2: 1.05,
    3: 1.00,
    4: 0.97,
    5: 1.01,
    6: 0.95,
    7: 0.94,
    8: 1.04,
    9: 1.06,
    10: 1.08,
    11: 1.12,
    12: 1.15,
}

MONTH_CVR_MULTIPLIER = {
    1: 0.96,
    2: 1.10,
    3: 1.00,
    4: 0.97,
    5: 1.02,
    6: 0.93,
    7: 0.92,
    8: 1.03,
    9: 1.05,
    10: 1.08,
    11: 1.20,
    12: 1.22,
}

# 节日/事件叠加效果（乘法调整）
PEAK_EVENTS = [
    {"start": datetime(2024, 2, 10), "end": datetime(2024, 2, 18), "spend": 1.10, "ctr": 1.12, "cvr": 1.25},  # 情人节
    {"start": datetime(2024, 5, 1), "end": datetime(2024, 5, 12), "spend": 1.05, "ctr": 1.05, "cvr": 1.10},   # 母亲节
    {"start": datetime(2024, 8, 1), "end": datetime(2024, 8, 25), "spend": 1.08, "ctr": 1.06, "cvr": 1.08},   # 返校季
    {"start": datetime(2024, 11, 20), "end": datetime(2024, 11, 30), "spend": 1.30, "ctr": 1.20, "cvr": 1.40}, # 黑五/网一
    {"start": datetime(2024, 12, 10), "end": datetime(2024, 12, 31), "spend": 1.25, "ctr": 1.18, "cvr": 1.32}, # 假日季
]


def get_multipliers(date: pd.Timestamp):
    """根据月份和事件获取 spend/ctr/cvr 调整系数"""
    spend_mult = MONTH_SPEND_MULTIPLIER.get(date.month, 1.0)
    ctr_mult = MONTH_CTR_MULTIPLIER.get(date.month, 1.0)
    cvr_mult = MONTH_CVR_MULTIPLIER.get(date.month, 1.0)

    for event in PEAK_EVENTS:
        if event["start"] <= date <= event["end"]:
            spend_mult *= event.get("spend", 1.0)
            ctr_mult *= event.get("ctr", 1.0)
            cvr_mult *= event.get("cvr", 1.0)

    return spend_mult, ctr_mult, cvr_mult


# ==================== Meta Ads 数据生成 ====================
print("Generating Meta Ads data...")

meta_campaigns = [
    {"name": "Always_On_Prospecting", "budget": 360, "ctr": 0.026, "cvr": 0.020, "has_conversion": True, "start_date": START_DATE},
    {"name": "Prospecting_Lookalike_A", "budget": 410, "ctr": 0.030, "cvr": 0.023, "has_conversion": True, "start_date": START_DATE},
    {"name": "Retargeting_Core", "budget": 320, "ctr": 0.048, "cvr": 0.055, "has_conversion": True, "start_date": START_DATE},
    {"name": "Brand_Awareness_Q1", "budget": 250, "ctr": 0.012, "cvr": 0.004, "has_conversion": False, "start_date": START_DATE},
    {"name": "Spring_Promo_Video", "budget": 380, "ctr": 0.034, "cvr": 0.026, "has_conversion": True, "start_date": datetime(2024, 3, 1)},
    {"name": "Summer_Collections", "budget": 300, "ctr": 0.029, "cvr": 0.020, "has_conversion": True, "start_date": datetime(2024, 6, 1)},
    {"name": "Back_to_School_Push", "budget": 420, "ctr": 0.036, "cvr": 0.027, "has_conversion": True, "start_date": datetime(2024, 8, 1)},
    {"name": "Holiday_Peak_Sales", "budget": 620, "ctr": 0.045, "cvr": 0.038, "has_conversion": True, "start_date": datetime(2024, 11, 1)},
    {"name": "Creative_Test_Variant_A", "budget": 160, "ctr": 0.028, "cvr": 0.021, "has_conversion": True, "start_date": datetime(2024, 2, 20)},
    {"name": "Creative_Test_Variant_B", "budget": 160, "ctr": 0.032, "cvr": 0.024, "has_conversion": True, "start_date": datetime(2024, 2, 20)},
    {"name": "Weekend_Flash_Sale", "budget": 200, "ctr": 0.040, "cvr": 0.030, "has_conversion": True, "start_date": START_DATE, "pause_weekend": True},
    {"name": "Email_List_Retargeting", "budget": 290, "ctr": 0.050, "cvr": 0.058, "has_conversion": True, "start_date": START_DATE},
]

meta_records = []

for campaign in meta_campaigns:
    for date in DATE_RANGE:
        if date < campaign["start_date"]:
            continue

        spend_mult, ctr_mult, cvr_mult = get_multipliers(date)

        # 一些 campaign 周末暂停
        if campaign.get("pause_weekend", False) and date.weekday() >= 5:
            continue

        # 展示量（受预算与季节影响）
        base_impressions = campaign["budget"] * 55
        impressions = int(np.random.normal(base_impressions * spend_mult, base_impressions * 0.18))
        impressions = max(150, impressions)

        # CTR
        ctr = max(0.001, np.random.normal(campaign["ctr"] * ctr_mult, campaign["ctr"] * 0.22))
        clicks = int(impressions * ctr)

        # 花费（与季节、事件相关）
        spend = np.random.normal(campaign["budget"] * spend_mult, campaign["budget"] * 0.18)
        spend = round(max(15, spend), 2)

        # 转化逻辑
        if campaign["has_conversion"]:
            cvr = max(0.001, np.random.normal(campaign["cvr"] * cvr_mult, campaign["cvr"] * 0.28))
            conversions = int(clicks * cvr)
            conversions = max(0, conversions)
            conversion_value = conversions * 85  # 平均客单价 85 美元
            cpa = round(spend / conversions, 2) if conversions > 0 else "--"
        else:
            conversions = "--"
            conversion_value = "--"
            cpa = "--"

        # 周末普遍会降温 15%
        if date.weekday() >= 5:
            impressions = int(impressions * 0.85)
            clicks = int(clicks * 0.85)
            spend = round(spend * 0.88, 2)
            if conversions not in ["--", 0]:
                conversions = int(conversions * 0.88)
                conversion_value = conversions * 85 if conversions > 0 else 0
                cpa = round(spend / max(1, conversions), 2)

        # 小样本导致高 CPA 的异常
        if conversions not in ["--", 0] and conversions < 3:
            cpa = round(spend / max(1, conversions), 2)

        reach = int(impressions * np.random.uniform(0.68, 0.82))

        meta_records.append({
            "Reporting starts": date.strftime("%Y-%m-%d"),
            "Reporting ends": date.strftime("%Y-%m-%d"),
            "Campaign name": campaign["name"],
            "Amount spent (USD)": spend,
            "Impressions": impressions,
            "Link clicks": clicks,
            "Purchases": conversions,
            "Cost per purchase (USD)": cpa,
            "Purchase conversion value (USD)": conversion_value,
            "Reach": reach,
        })

meta_df = pd.DataFrame(meta_records)

# 模拟重新导出导致的重复
duplicate_indices = random.sample(range(len(meta_df)), 30)
duplicates = meta_df.iloc[duplicate_indices].copy()
for idx in duplicates.index:
    if duplicates.loc[idx, "Purchases"] not in ["--", 0]:
        adjustment = random.randint(-2, 3)
        new_conversions = max(0, duplicates.loc[idx, "Purchases"] + adjustment)
        duplicates.loc[idx, "Purchases"] = new_conversions
        if new_conversions > 0:
            spend = duplicates.loc[idx, "Amount spent (USD)"]
            duplicates.loc[idx, "Cost per purchase (USD)"] = round(spend / new_conversions, 2)
            duplicates.loc[idx, "Purchase conversion value (USD)"] = new_conversions * 85

meta_df = pd.concat([meta_df, duplicates], ignore_index=True)
meta_df.to_csv("data/raw/meta_ads_raw.csv", index=False)
print(f"[OK] Meta Ads: {len(meta_df)} rows saved")


# ==================== Google Ads 数据生成 ====================
print("Generating Google Ads data...")

google_campaigns = [
    {"name": "Search_Brand_Exact", "id": "1234567890", "budget": 370, "ctr": 0.155, "cvr": 0.090, "start_date": START_DATE},
    {"name": "Search_Generic_Broad", "id": "1234567891", "budget": 420, "ctr": 0.032, "cvr": 0.019, "start_date": START_DATE},
    {"name": "Display_Retargeting", "id": "1234567892", "budget": 260, "ctr": 0.009, "cvr": 0.034, "start_date": START_DATE},
    {"name": "Shopping_Product_Feed", "id": "1234567893", "budget": 480, "ctr": 0.047, "cvr": 0.030, "start_date": START_DATE},
    {"name": "Video_YouTube_Awareness", "id": "1234567894", "budget": 320, "ctr": 0.016, "cvr": 0.008, "start_date": START_DATE},
    {"name": "Search_Competitor_Keywords", "id": "1234567895", "budget": 340, "ctr": 0.029, "cvr": 0.016, "start_date": START_DATE},
    {"name": "Display_Lookalike", "id": "1234567896", "budget": 290, "ctr": 0.013, "cvr": 0.023, "start_date": datetime(2024, 1, 15)},
    {"name": "Search_Long_Tail", "id": "1234567897", "budget": 240, "ctr": 0.039, "cvr": 0.026, "start_date": START_DATE},
    {"name": "RLSA_Past_Visitors", "id": "1234567898", "budget": 280, "ctr": 0.053, "cvr": 0.044, "start_date": START_DATE},
    {"name": "Smart_Shopping", "id": "1234567899", "budget": 400, "ctr": 0.042, "cvr": 0.032, "start_date": datetime(2024, 1, 25)},
    {"name": "Holiday_Gift_Search", "id": "1234567800", "budget": 520, "ctr": 0.050, "cvr": 0.040, "start_date": datetime(2024, 10, 1)},
]

google_records = []

for campaign in google_campaigns:
    for date in DATE_RANGE:
        if date < campaign["start_date"]:
            continue

        spend_mult, ctr_mult, cvr_mult = get_multipliers(date)

        impressions = int(np.random.normal(campaign["budget"] * 48 * spend_mult, campaign["budget"] * 9))
        impressions = max(120, impressions)

        ctr = max(0.001, np.random.normal(campaign["ctr"] * ctr_mult, campaign["ctr"] * 0.20))
        clicks = int(impressions * ctr)

        cost = round(max(12, np.random.normal(campaign["budget"] * spend_mult, campaign["budget"] * 0.18)), 2)

        cvr = max(0.001, np.random.normal(campaign["cvr"] * cvr_mult, campaign["cvr"] * 0.24))
        raw_conversions = clicks * cvr

        # Google 的隐私保护：小于 10 的转化可能显示为 < 10
        if raw_conversions < 10 and random.random() < 0.35:
            conversions_display = "< 10"
            conv_rate_display = "--"
            cost_per_conv_display = "--"
            conv_value_display = "--"
        else:
            conversions = int(raw_conversions)
            conversions_display = conversions
            conv_rate = (conversions / clicks * 100) if clicks > 0 else 0
            conv_rate_display = f"{conv_rate:.2f}%"
            if conversions > 0:
                cost_per_conv_display = round(cost / conversions, 2)
                conv_value_display = conversions * 85
            else:
                cost_per_conv_display = "--"
                conv_value_display = "--"

        # 预算用尽的情况：当天后半段投放停止，曝光骤降
        if random.random() < 0.06:
            impressions = int(impressions * 0.6)
            clicks = int(clicks * 0.6)

        # 数据延迟：随机 2% 的行将 Conversions 显示为 --
        if random.random() < 0.02:
            conversions_display = "--"
            conv_rate_display = "--"
            cost_per_conv_display = "--"
            conv_value_display = "--"

        google_records.append({
            "Day": date.strftime("%Y-%m-%d"),
            "Campaign": campaign["name"],
            "Campaign ID": campaign["id"],
            "Impr.": impressions,
            "Clicks": clicks,
            "Cost": round(cost, 2),
            "Conversions": str(conversions_display),
            "Conv. rate": conv_rate_display,
            "Cost / conv.": str(cost_per_conv_display),
            "Conv. value": str(conv_value_display),
        })

google_df = pd.DataFrame(google_records)

# 保存时添加 metadata 行（模拟真实导出）
with open("data/raw/google_ads_raw.csv", "w", newline="") as f:
    f.write("Campaign performance report\n")
    f.write("Downloaded: 2024-12-31 23:59:59 PST\n\n")
    google_df.to_csv(f, index=False)

print(f"[OK] Google Ads: {len(google_df)} rows saved")


# ==================== TikTok Ads 数据生成 ====================
print("Generating TikTok Ads data...")

tiktok_adgroups = [
    {"campaign": "New_Year_Sale", "ad_group": "Lookalike_Audience_1", "budget": 320, "ctr": 0.032, "cvr": 0.028, "start_date": START_DATE},
    {"campaign": "New_Year_Sale", "ad_group": "Interest_Fashion", "budget": 300, "ctr": 0.030, "cvr": 0.027, "start_date": START_DATE},
    {"campaign": "Spring_Collections", "ad_group": "Broad_Interest_Apparel", "budget": 280, "ctr": 0.029, "cvr": 0.024, "start_date": datetime(2024, 3, 1)},
    {"campaign": "Summer_Vibes", "ad_group": "Spark_Addicts", "budget": 260, "ctr": 0.027, "cvr": 0.022, "start_date": datetime(2024, 6, 1)},
    {"campaign": "Back_to_School", "ad_group": "Student_Device", "budget": 310, "ctr": 0.031, "cvr": 0.026, "start_date": datetime(2024, 8, 1)},
    {"campaign": "Holiday_Mega_Sale", "ad_group": "Gift_Shoppers", "budget": 380, "ctr": 0.037, "cvr": 0.032, "start_date": datetime(2024, 11, 1)},
    {"campaign": "Creative_Test_Video", "ad_group": "UGC_Creator_A", "budget": 200, "ctr": 0.028, "cvr": 0.021, "start_date": datetime(2024, 2, 15)},
    {"campaign": "Creative_Test_Video", "ad_group": "UGC_Creator_B", "budget": 200, "ctr": 0.030, "cvr": 0.022, "start_date": datetime(2024, 2, 15)},
]

tiktok_records = []

for group in tiktok_adgroups:
    for date in DATE_RANGE:
        if date < group["start_date"]:
            continue

        spend_mult, ctr_mult, cvr_mult = get_multipliers(date)

        cost = np.random.normal(group["budget"] * spend_mult, group["budget"] * 0.22)
        cost = round(max(6, cost), 2)

        impressions = int(np.random.normal(group["budget"] * 62 * spend_mult, group["budget"] * 14))
        impressions = max(90, impressions)

        ctr = max(0.001, np.random.normal(group["ctr"] * ctr_mult, group["ctr"] * 0.22))
        clicks = int(impressions * ctr)

        cvr = max(0.001, np.random.normal(group["cvr"] * cvr_mult, group["cvr"] * 0.26))
        conversions = int(clicks * cvr)
        conversions = max(0, conversions)

        days_active = (date - group["start_date"]).days
        if days_active < 5:
            learning_status = "Learning"
        elif random.random() < 0.07:
            learning_status = "Learning"
        elif random.random() < 0.05:
            learning_status = "Limited"
        else:
            learning_status = "Active"

        if random.random() < 0.05:
            cost = 0

        video_views = int(impressions * np.random.uniform(0.45, 0.72))
        video_actions = int(video_views * np.random.uniform(0.65, 0.9))

        revenue = conversions * 80
        cpa = round(cost / conversions, 2) if conversions > 0 else "--"
        ctr_pct = f"{(clicks / impressions * 100):.2f}%" if impressions > 0 else "0.00%"
        cvr_pct = f"{(conversions / clicks * 100):.2f}%" if clicks > 0 else "0.00%"

        tiktok_records.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Campaign Name": group["campaign"],
            "Ad Group Name": group["ad_group"],
            "Cost": round(cost, 2),
            "Impressions": impressions,
            "Clicks": clicks,
            "Conversions": conversions,
            "CPA": cpa if isinstance(cpa, str) else round(cpa, 2),
            "CTR": ctr_pct,
            "CVR": cvr_pct,
            "Video Views": video_views,
            "Video Play Actions": video_actions,
            "Learning Status": learning_status,
        })

tiktok_df = pd.DataFrame(tiktok_records)

tiktok_df["Conversions"] = tiktok_df["Conversions"].astype(object)
tiktok_df["CPA"] = tiktok_df["CPA"].astype(object)

mask_missing = (tiktok_df["Conversions"] == 0) & (np.random.rand(len(tiktok_df)) < 0.05)
tiktok_df.loc[mask_missing, "Conversions"] = "--"
tiktok_df.loc[mask_missing, "CPA"] = "--"

tiktok_df.to_csv("data/raw/tiktok_ads_raw.csv", index=False)
print(f"[OK] TikTok Ads: {len(tiktok_df)} rows saved")

print("✅ Raw data generation complete.")
