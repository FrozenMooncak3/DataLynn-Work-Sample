# DataLynn 营销分析工作样本

> 复刻实习期间的广告投放分析链路：数据清洗 → ROAS 建模 → 创意 A/B 测试 → Power BI 可视化。仓库开箱即带数据与脚本，可直接运行或用于面试讲解。

---

## 为什么值得看
- **端到端自动化**：`scripts/run_all_pipelines.py` 一次跑完 Week1–Week3，输出干净数据、模型指标与测试报告。
- **模块化代码**：所有 Notebook 逻辑都已沉淀到 `src/pipelines/`，可直接嵌入生产任务。
- **随仓库附带数据**：`data/` 中包含最新生成的模拟 CSV，面试官无需额外准备。
- **Power BI 指南齐备**：附 DAX 配方与页面布局，可快速复现成品仪表盘。

---

## 目录速览
```
├── README.md                  # 本说明
├── requirements.txt           # Python 依赖
├── data/                      # 原始/清洗后/AB 测试数据 + 数据字典
├── scripts/                   # Week1-3 流水线脚本 & 质量检查
├── src/                       # 模块化流水线实现
├── output/                    # 核心图表与报告（可直接引用到简历/汇报）
└── powerbi/                   # PB 仪表盘操作说明与截图占位
```

---

## 快速上手

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python scripts/run_all_pipelines.py
```

> `run_all_pipelines.py` 会串行执行三个阶段脚本，覆盖写入 `data/processed/` 与 `output/`。如需单独调试，可运行 `run_week{1,2,3}_pipeline.py`。

运行后你将得到：

- `data/processed/*.csv`：三平台清洗结果与整合表。
- `output/reports/random_forest_roas_metrics.json`：模型评估。
- `output/reports/ab_test_report.md`、`output/figures/*.png`：A/B 测试结论与图表。

---

## 数据说明

仓库中已包含最新模拟数据，方便开箱演示：

- `data/raw/`: 三个平台的原始导出（预埋缺失、隐私脱敏、重复行等问题）。
- `data/processed/`: Week1 流水线清洗后的统一 schema。
- `data/ab_test/`: Week3 创意测试数据。
- `data/DATA_DICTIONARY.md`: 每个字段的含义与单位。

如需刷新数据，可再次运行生成脚本，旧文件会被覆盖：

```bash
python scripts/generate_raw_data.py
python scripts/run_all_pipelines.py
```

---

## 流水线与自动化

| 阶段 | 入口脚本 | 核心模块 | 主要输出 |
|------|----------|----------|----------|
| Week 1 — 数据工程 | `scripts/run_week1_pipeline.py` | `src/pipelines/week1_data_prep.py` | `data/processed/*.csv` |
| Week 2 — ROAS 建模 | `scripts/run_week2_pipeline.py` | `src/pipelines/week2_roas_modeling.py` | `output/reports/random_forest_roas_metrics.json` |
| Week 3 — A/B 测试 | `scripts/run_week3_pipeline.py` | `src/pipelines/week3_ab_testing.py` | `output/reports/ab_test_*.csv` / `.md`、`output/figures/*.png` |

所有入口脚本均可被调度系统调用，例如：

- **Cron / Windows 计划任务**：在每日 8:00 执行 `python scripts/run_all_pipelines.py`，随后 Power BI Desktop “刷新” 即可呈现最新指标。
- **CI/CD（GitHub Actions）**：配置 Python runner，运行脚本后将 CSV/图表上传至 GitHub Release 或云存储，再触发 Power BI Service 刷新（详细差异见 `docs/production_vs_github.md`）。

---

## Power BI 仪表盘指南

> 完整步骤详见 `docs/WEEK4_POWERBI_GUIDE.md`，此处给出核心提要与 DAX 配方。

1. **加载数据**：Get Data → Text/CSV → `data/processed/integrated_data.csv`。确认 `date` 设为 Date，指标列为 Decimal。
2. **日期维度表**：
   ```DAX
   DateTable =
   CALENDAR(MIN(integrated_data[date]), MAX(integrated_data[date]))
   ```
   衍生列：
   ```DAX
   Year = YEAR(DateTable[Date])
   Quarter = "Q" & FORMAT(DateTable[Date], "Q")
   Month = FORMAT(DateTable[Date], "MMMM")
   MonthNum = MONTH(DateTable[Date])
   DayOfWeek = FORMAT(DateTable[Date], "dddd")
   IsWeekend = IF(WEEKDAY(DateTable[Date], 2) >= 6, "Weekend", "Weekday")
   ```
   在模型视图中将 `DateTable[Date]` 与 `integrated_data[date]` 建立一对多关系。
3. **度量值 (Measures)**：
   ```DAX
   Total Spend = SUM(integrated_data[spend])
   Total Revenue = SUM(integrated_data[revenue])
   Total Conversions = SUM(integrated_data[conversions])
   Average ROAS = AVERAGE(integrated_data[roas])

   ROAS (Calculated) = DIVIDE([Total Revenue], [Total Spend], 0)
   CTR (Calculated)  = DIVIDE(SUM(integrated_data[clicks]), SUM(integrated_data[impressions]), 0)
   CVR (Calculated)  = DIVIDE([Total Conversions], SUM(integrated_data[clicks]), 0)
   CPA (Calculated)  = DIVIDE([Total Spend], [Total Conversions], 0)
   ```
4. **页面设计**：
   - **Overview**：KPI 卡片（Spend/Revenue/ROAS/Conversions）、ROAS 趋势折线、Spend vs ROAS 组合图、CTR×CVR 气泡图 + 切片器（平台、季度）。
   - **Platform Comparison**：堆叠柱对比季度转化、Spend vs ROAS 组合图、Campaign 明细表（带条件格式）。
   - **Time Analysis**：Month × DayOfWeek 热力图、瀑布图/条形图分析季节性，支持平台筛选。
   - **A/B Test（可选）**：Get Data 导入 `output/reports/ab_test_summary.csv` 等，制作表格 & 趋势线。
5. **交付**：保存为 `powerbi/datalynn_dashboard.pbix`，在 `powerbi/screenshots/` 截取页面 PNG，可录制 `demo.gif` 演示筛选动作。

刷新策略：流水线覆盖写入 CSV 后，在 Power BI Desktop/Service 中执行 Refresh，即可读取最新结果。

---

## Notebook（可选阅读）

为方便审阅者快速查看中间结果，提供两份与流水线一致的“干净” Notebook：

- `notebooks/02_roas_model_pipeline.ipynb`
- `notebooks/04_ab_test_analysis.ipynb`

它们仅展示关键步骤和输出，所有核心逻辑仍以 `src/` 为准。

---

## 真实环境 vs GitHub 版本

- 真实实习中的原始数据、广告 ID 等均为保密；本仓库使用 Faker + 经验规则生成的可复现模拟数据。
- Power BI 在线版需借助 Personal Gateway 或云数据仓库；此处改为本地刷新流程，详见 `docs/production_vs_github.md`。
- 自动化策略（CI、调度脚本）可按团队基础设施落地，本仓库提供的脚本接口已经满足接入要求。

---

