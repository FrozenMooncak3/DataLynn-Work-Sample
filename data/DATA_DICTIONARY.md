# 数据字典

## Meta Ads (meta_ads_raw.csv)

| 字段名 | 含义 | 数据类型 | 备注 |
|--------|------|---------|------|
| Reporting starts | 报告开始日期 | 日期 (YYYY-MM-DD) | 和Reporting ends相同 |
| Reporting ends | 报告结束日期 | 日期 (YYYY-MM-DD) | 和Reporting starts相同 |
| Campaign name | Campaign名称 | 文本 | |
| Amount spent (USD) | 广告花费 | 数字 | 单位：美元 |
| Impressions | 展示次数 | 整数 | |
| Link clicks | 链接点击次数 | 整数 | Meta特有概念 |
| Purchases | 购买转化数 | 整数或"--" | "--"表示无转化追踪 |
| Cost per purchase (USD) | 单次购买成本 | 数字或"--" | CPA |
| Purchase conversion value (USD) | 购买转化价值 | 数字或"--" | 假设AOV=$80 |
| Reach | 触达人数 | 整数 | 约为Impressions的70-85% |

**已知问题**:
- Brand_Awareness_Q1 campaign没有转化追踪（Purchases列全是"--"）
- 有5行重复数据（重新导出导致）
- 某些周末的CPA异常高（样本量小）

---

## Google Ads (google_ads_raw.csv)

| 字段名 | 含义 | 数据类型 | 备注 |
|--------|------|---------|------|
| Day | 日期 | 日期 (YYYY-MM-DD) | |
| Campaign | Campaign名称 | 文本 | |
| Campaign ID | Campaign唯一ID | 文本 | |
| Impr. | 展示次数 | 整数 | 缩写！ |
| Clicks | 点击次数 | 整数 | |
| Cost | 广告花费 | 数字 | 单位：美元 |
| Conversions | 转化数 | 数字或"< 10" | 隐私保护 |
| Conv. rate | 转化率 | 文本 (百分比) | 如"5.13%" |
| Cost / conv. | 单次转化成本 | 数字或"--" | CPA |
| Conv. value | 转化价值 | 数字或"--" | |

**已知问题**:
- **前3行是metadata**，不是数据！需要跳过
- 某些Conversions是"< 10"（隐私保护，无法使用）
- Conv. rate是字符串格式（"5.13%"），需要转换成0.0513
- Search_Brand_Exact的CTR高达15%（正常，因为是品牌词）

---

## TikTok Ads (tiktok_ads_raw.csv)

| 字段名 | 含义 | 数据类型 | 备注 |
|--------|------|---------|------|
| Date | 日期 | 日期 (YYYY-MM-DD) | |
| Campaign Name | Campaign名称 | 文本 | |
| Ad Group Name | Ad Group名称 | 文本 | TikTok是三层结构 |
| Cost | 广告花费 | 数字 | 单位：美元 |
| Impressions | 展示次数 | 整数 | |
| Clicks | 点击次数 | 整数 | |
| Conversions | 转化数 | 整数或"--" | |
| CPA | 单次转化成本 | 数字或"--" | |
| CTR | 点击率 | 文本 (百分比) | 如"3.36%" |
| CVR | 转化率 | 文本 (百分比) | 如"2.15%" |
| Video Views | 视频观看数 | 整数 | TikTok特有 |
| Video Play Actions | 视频播放动作数 | 整数 | TikTok特有 |
| Learning Status | 学习状态 | 文本 | "Learning"或"Active" |

**已知问题**:
- 学习期（Learning）的数据波动大，前7天不稳定
- 某些天Cost=0但有Impressions（数据延迟）
- 学习期某些Conversions可能是"--"（数据不全）
- CTR、CVR是字符串格式，需要转换

---

## 统一指标计算公式

**CTR (Click-Through Rate)**: Clicks / Impressions × 100%

**CVR (Conversion Rate)**: Conversions / Clicks × 100%

**CPA (Cost Per Acquisition)**: Spend / Conversions

**ROAS (Return on Ad Spend)**: Revenue / Spend
- Revenue = Conversions × AOV ($80)

---

**生成时间**: 2024-04-01
**数据时间范围**: 2024-01-01 至 2024-03-31 (Q1)
