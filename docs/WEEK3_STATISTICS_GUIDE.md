# 📊 Week 3: 统计分析（预算优化 + A/B测试）

> 状态：草稿（待模型结果与A/B数据准备完成后完善）

---

## ⚠️ 开始前必读

**在开始Week 3之前，请确认**：
- ✅ Week 2已完成（训练好的模型已保存在 `output/models/`）
- ✅ 已阅读 `ARCHITECTURE.md` 的Week 2-3部分
- ✅ Python环境已安装 `scipy` 库

---

## 🎯 本周学习目标

通过Week 3，你将学会：

### Part 1: 预算优化（基于ML模型）
- 使用 `scipy.optimize` 求解最优预算分配
- 定义目标函数和约束条件
- 理解优化算法（SLSQP）
- 向业务方解释优化结果

### Part 2: A/B测试分析
- 设计A/B测试（控制组 vs 实验组）
- 使用t检验判断显著性
- 计算p-value并解释
- 处理学习期（Learning Period）
- 向业务方汇报测试结果

---

## 📦 依赖清单

```bash
pip install pandas numpy scipy matplotlib seaborn
```

**版本要求**：
- scipy >= 1.11.1
- pandas >= 2.0.3
- numpy >= 1.24.3

---

## 🚀 Day 4 工作流程

### Part 1: 预算优化（4-5小时）

```
08:00-09:00: 理解优化问题（数学建模）
09:00-11:00: 编写目标函数和约束条件
11:00-12:00: 运行优化算法，验证结果
12:00-13:00: 午休
13:00-15:00: A/B测试数据准备和分析
15:00-16:00: t检验和显著性判断
16:00-17:00: 生成测试报告
```

---

## 📝 Part 1: 预算优化

### 业务场景（来自Sarah的邮件）

```
From: Sarah Chen <sarah.chen@datalynn.com>
To: You <intern@datalynn.com>
Date: Monday, March 15, 2024, 9:00 AM
Subject: 下个月预算分配

Hi [你的名字],

CFO批准了下个月$50,000的广告预算。我需要你帮忙决定如何分配到三个平台（Meta, Google, TikTok）才能最大化ROAS。

**约束条件**：
- 总预算不能超过$50,000
- 每个平台至少分配$5,000（保持曝光）
- 任何平台不能超过$30,000（风险分散）

你上周训练的ROAS预测模型应该能帮到你！周五前给我一个分配方案。

Best,
Sarah
```

---

### Step 1: 加载训练好的模型（30分钟）

创建新的Notebook: `notebooks/03_budget_optimization.ipynb`

```python
import pandas as pd
import numpy as np
import pickle
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import seaborn as sns

# 加载Week 2训练的模型
with open('../output/models/random_forest_model.pkl', 'rb') as f:
    model = pickle.load(f)

print("✅ 模型已加载")
print(f"模型类型: {type(model)}")

# 加载模型指标
import json
with open('../output/models/model_metrics.json', 'r') as f:
    metrics = json.load(f)

print(f"\n模型性能:")
print(f"MAE: {metrics['mae']:.4f}")
print(f"R²: {metrics['r2']:.4f}")
```

---

### Step 2: 理解优化问题（1小时）

#### 数学建模

**优化目标**：
```
最大化: Total_ROAS = ROAS_Meta + ROAS_Google + ROAS_TikTok
```

**决策变量**：
```
x = [budget_Meta, budget_Google, budget_TikTok]
```

**约束条件**：
```
1. budget_Meta + budget_Google + budget_TikTok = 50000  (等式约束)
2. budget_Meta >= 5000                                  (不等式约束)
3. budget_Google >= 5000                                (不等式约束)
4. budget_TikTok >= 5000                                (不等式约束)
5. budget_Meta <= 30000                                 (不等式约束)
6. budget_Google <= 30000                               (不等式约束)
7. budget_TikTok <= 30000                               (不等式约束)
```

**引导问题**：
- ❓ 如果没有约束，最优策略是什么？（提示：全投到ROAS最高的平台）
- ❓ 为什么要设置最小预算$5,000？（提示：保持曝光、测试效果）
- ❓ 为什么要设置最大预算$30,000？（提示：风险分散、市场饱和）

---

### Step 3: 准备预测函数（1-2小时）

#### 创建特征函数

```python
def create_prediction_features(budget, platform, historical_data):
    """
    为给定预算和平台创建预测特征

    参数:
        budget: 预算金额
        platform: 平台名称（'Meta', 'Google', 'TikTok'）
        historical_data: 历史数据（用于计算滞后特征）

    返回:
        特征向量（与训练时特征列顺序一致）
    """
    # 筛选该平台的历史数据
    platform_data = historical_data[historical_data['platform'] == platform]

    # 计算滞后特征（过去7天平均值）
    spend_last_7d = platform_data['spend'].tail(7).mean()
    ctr_last_7d = platform_data['ctr'].tail(7).mean()
    cvr_last_7d = platform_data['cvr'].tail(7).mean()
    cpa_last_7d = platform_data['cpa'].tail(7).mean()

    # 时间特征（假设预算用于下周一）
    day_of_week = 0  # 周一
    is_weekend = 0   # 工作日
    month = 4        # 4月

    # 平台one-hot编码
    platform_meta = 1 if platform == 'Meta' else 0
    platform_google = 1 if platform == 'Google' else 0
    platform_tiktok = 1 if platform == 'TikTok' else 0

    # 组合特征（顺序必须与训练时一致！）
    features = [
        spend_last_7d,
        ctr_last_7d,
        cvr_last_7d,
        cpa_last_7d,
        day_of_week,
        is_weekend,
        month,
        platform_meta,
        platform_google,
        platform_tiktok
    ]

    return np.array(features).reshape(1, -1)
```

**任务**：
- 你的代码：读取 `integrated_data.csv` 作为历史数据
- 你的代码：测试函数，预测"Meta平台投$10,000的预期ROAS"

```python
# 你的代码
# 读取历史数据
df = pd.read_csv('../data/processed/integrated_data.csv')

# 测试预测
features_meta = create_prediction_features(10000, 'Meta', df)
predicted_roas = model.predict(features_meta)[0]

print(f"预测结果: Meta平台投$10,000 → ROAS = {predicted_roas:.2f}")
```

---

### Step 4: 定义目标函数和约束（1小时）

```python
def objective(budgets):
    """
    目标函数：返回负的总ROAS（因为minimize求最小值，我们需要最大化）

    参数:
        budgets: [budget_Meta, budget_Google, budget_TikTok]

    返回:
        -total_roas（负号因为我们要最大化）
    """
    # 预测每个平台的ROAS
    features_meta = create_prediction_features(budgets[0], 'Meta', df)
    features_google = create_prediction_features(budgets[1], 'Google', df)
    features_tiktok = create_prediction_features(budgets[2], 'TikTok', df)

    roas_meta = model.predict(features_meta)[0]
    roas_google = model.predict(features_google)[0]
    roas_tiktok = model.predict(features_tiktok)[0]

    # 总ROAS
    total_roas = roas_meta + roas_google + roas_tiktok

    # 返回负值（因为minimize）
    return -total_roas


# 约束条件
constraints = [
    # 等式约束：总预算 = $50,000
    {'type': 'eq', 'fun': lambda x: sum(x) - 50000},

    # 不等式约束：每个平台至少$5,000
    {'type': 'ineq', 'fun': lambda x: x[0] - 5000},   # Meta >= 5000
    {'type': 'ineq', 'fun': lambda x: x[1] - 5000},   # Google >= 5000
    {'type': 'ineq', 'fun': lambda x: x[2] - 5000},   # TikTok >= 5000

    # 不等式约束：每个平台最多$30,000
    {'type': 'ineq', 'fun': lambda x: 30000 - x[0]},  # Meta <= 30000
    {'type': 'ineq', 'fun': lambda x: 30000 - x[1]},  # Google <= 30000
    {'type': 'ineq', 'fun': lambda x: 30000 - x[2]}   # TikTok <= 30000
]

# 变量边界
bounds = [
    (5000, 30000),   # Meta
    (5000, 30000),   # Google
    (5000, 30000)    # TikTok
]
```

**引导问题**：
- ❓ 为什么目标函数返回负值？
- ❓ `'type': 'eq'` 和 `'type': 'ineq'` 有什么区别？
- ❓ `lambda x: x[0] - 5000` 是什么意思？（提示：x[0] - 5000 >= 0 即 x[0] >= 5000）

---

### Step 5: 运行优化算法（30分钟）

```python
# 初始猜测（平均分配）
x0 = [16666, 16666, 16668]

print("="*50)
print("开始优化...")
print(f"初始预算分配: {x0}")
print(f"初始总ROAS预测: {-objective(x0):.2f}")
print("="*50)

# 运行优化
result = minimize(
    objective,
    x0,
    method='SLSQP',           # 序列最小二乘规划
    bounds=bounds,
    constraints=constraints,
    options={'maxiter': 100, 'disp': True}
)

# 输出结果
print("\n优化完成！")
print("="*50)
print("最优预算分配:")
print(f"Meta:    ${result.x[0]:,.0f}")
print(f"Google:  ${result.x[1]:,.0f}")
print(f"TikTok:  ${result.x[2]:,.0f}")
print(f"总预算:  ${sum(result.x):,.0f}")
print(f"\n预期总ROAS: {-result.fun:.2f}")
print("="*50)
```

**引导问题**：
- ❓ 优化结果是否满足所有约束？（总和=$50K，每个平台$5K-$30K）
- ❓ 哪个平台分配的预算最多？为什么？
- ❓ 如果放宽约束（如允许某平台最多$40K），结果会改变吗？

---

### Step 6: 可视化优化结果（1小时）

```python
# 你的代码
# 任务1：绘制优化前后的预算分配对比（柱状图）
# 提示：
platforms = ['Meta', 'Google', 'TikTok']
initial_budgets = x0
optimal_budgets = result.x

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# 左图：预算分配对比
# 你的代码

# 右图：预期ROAS对比
# 你的代码（需要预测初始分配和最优分配的ROAS）

plt.tight_layout()
plt.savefig('../output/figures/budget_optimization.png', dpi=300)
plt.show()
```

---

### Step 7: 生成优化报告（30分钟）

```python
# 你的代码
# 任务：生成一个Markdown报告，保存到 output/reports/budget_optimization_report.md
# 包含：
# - 优化目标
# - 约束条件
# - 初始方案 vs 最优方案
# - 预期ROAS提升
# - 业务建议

report = f"""
# 预算优化报告

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 优化目标
最大化总ROAS（给定$50,000预算）

## 约束条件
1. 总预算 = $50,000
2. 每个平台至少$5,000
3. 每个平台最多$30,000

## 优化结果

### 初始方案（平均分配）
| 平台 | 预算 | 预期ROAS |
|------|------|---------|
| Meta | ${x0[0]:,.0f} | {roas_meta_initial:.2f} |
| Google | ${x0[1]:,.0f} | {roas_google_initial:.2f} |
| TikTok | ${x0[2]:,.0f} | {roas_tiktok_initial:.2f} |
| **总计** | **${sum(x0):,.0f}** | **{-objective(x0):.2f}** |

### 最优方案
| 平台 | 预算 | 预期ROAS |
|------|------|---------|
| Meta | ${result.x[0]:,.0f} | {roas_meta_optimal:.2f} |
| Google | ${result.x[1]:,.0f} | {roas_google_optimal:.2f} |
| TikTok | ${result.x[2]:,.0f} | {roas_tiktok_optimal:.2f} |
| **总计** | **${sum(result.x):,.0f}** | **{-result.fun:.2f}** |

## 业务价值
- ROAS提升: {(-result.fun - (-objective(x0))):.2f} ({((-result.fun - (-objective(x0))) / (-objective(x0)) * 100):.1f}%)
- 预期额外收入: ${((-result.fun - (-objective(x0))) * 50000):,.0f}

## 建议
...
"""

# 保存报告
with open('../output/reports/budget_optimization_report.md', 'w', encoding='utf-8') as f:
    f.write(report)

print("✅ 报告已保存到 output/reports/budget_optimization_report.md")
```

---

## 📝 Part 2: A/B测试分析

### 业务场景（来自Sarah的Slack消息）

```
Sarah [10:15 AM]
@你 我们上个月在Meta上测试了两个创意：
- Creative A（现有创意）
- Creative B（新创意，设计团队推荐）

我需要你分析一下Creative B是否比A好。如果显著更好，我们就全面推广。

数据我放在了 data/ab_test/ 文件夹。记得排除学习期（前7天）！
```

---

### Step 1: 理解A/B测试设计（30分钟）

#### 什么是A/B测试？

**定义**: 将用户随机分成两组，对比不同策略的效果

**关键要素**:
1. **控制组（Control Group）**: Creative A（现有创意）
2. **实验组（Treatment Group）**: Creative B（新创意）
3. **随机分配**: 确保两组用户特征相似
4. **学习期（Learning Period）**: Meta/TikTok前7天算法还在学习，数据不稳定
5. **统计显著性**: 用t检验判断差异是否可靠

**引导问题**：
- ❓ 为什么要"随机分配"用户？不能直接让所有人看Creative B吗？
- ❓ 为什么要排除学习期？
- ❓ 什么是"统计显著性"？

---

### Step 2: 加载和探索数据（30分钟）

创建新的Notebook: `notebooks/04_ab_test_analysis.ipynb`

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 读取A/B测试数据
creative_a = pd.read_csv('../data/ab_test/creative_a.csv')
creative_b = pd.read_csv('../data/ab_test/creative_b.csv')

print("Creative A 数据:")
print(creative_a.head())
print(f"总行数: {len(creative_a)}")

print("\nCreative B 数据:")
print(creative_b.head())
print(f"总行数: {len(creative_b)}")
```

**你的代码**：
- 任务1：检查两个数据集的列名是否一致
- 任务2：检查是否有缺失值
- 任务3：可视化两个创意的ROAS趋势（折线图）

---

### Step 3: 排除学习期（30分钟）

```python
# 排除前7天（学习期）
creative_a_stable = creative_a[creative_a['day'] > 7].copy()
creative_b_stable = creative_b[creative_b['day'] > 7].copy()

print(f"Creative A（排除学习期后）: {len(creative_a_stable)}行")
print(f"Creative B（排除学习期后）: {len(creative_b_stable)}行")
```

**引导问题**：
- ❓ 学习期的ROAS通常比稳定期高还是低？
- ❓ 如果不排除学习期，会影响测试结果吗？

---

### Step 4: 计算关键指标（30分钟）

```python
# 定义要对比的指标
metrics = ['roas', 'cpa', 'ctr', 'cvr']

# 计算均值和标准差
summary = []
for metric in metrics:
    mean_a = creative_a_stable[metric].mean()
    std_a = creative_a_stable[metric].std()
    mean_b = creative_b_stable[metric].mean()
    std_b = creative_b_stable[metric].std()

    summary.append({
        'Metric': metric.upper(),
        'Creative A (Mean)': f"{mean_a:.4f}",
        'Creative A (Std)': f"{std_a:.4f}",
        'Creative B (Mean)': f"{mean_b:.4f}",
        'Creative B (Std)': f"{std_b:.4f}",
        'Difference': f"{mean_b - mean_a:.4f}"
    })

summary_df = pd.DataFrame(summary)
print(summary_df)
```

**引导问题**：
- ❓ 哪个创意的ROAS更高？
- ❓ 高多少？（绝对差异 vs 相对差异）
- ❓ 标准差大说明什么？（提示：波动性大）

---

### Step 5: t检验（1小时）

#### 什么是t检验？

**目的**: 判断两组数据的均值差异是否显著（不是偶然造成的）

**假设**:
- **零假设（H0）**: Creative A和Creative B的ROAS没有差异
- **备择假设（H1）**: Creative B的ROAS显著高于Creative A

**判断标准**: p-value < 0.05 → 拒绝零假设 → 差异显著

```python
from scipy import stats

results = []
for metric in metrics:
    # 提取两组数据
    data_a = creative_a_stable[metric]
    data_b = creative_b_stable[metric]

    # t检验
    t_stat, p_value = stats.ttest_ind(data_a, data_b)

    # 判断显著性
    significant = "Yes" if p_value < 0.05 else "No"

    # 计算效应量（Cohen's d）
    mean_diff = data_b.mean() - data_a.mean()
    pooled_std = np.sqrt((data_a.std()**2 + data_b.std()**2) / 2)
    cohens_d = mean_diff / pooled_std

    results.append({
        'Metric': metric.upper(),
        'Creative A': f"{data_a.mean():.4f}",
        'Creative B': f"{data_b.mean():.4f}",
        'Difference': f"{mean_diff:.4f}",
        't-statistic': f"{t_stat:.4f}",
        'p-value': f"{p_value:.4f}",
        'Significant (p<0.05)': significant,
        "Cohen's d": f"{cohens_d:.4f}"
    })

results_df = pd.DataFrame(results)
print(results_df)
```

**引导问题**：
- ❓ p-value=0.03是什么意思？（提示：3%概率是偶然）
- ❓ 如果ROAS的p-value=0.08，是否应该推广Creative B？
- ❓ Cohen's d=0.2是大效应还是小效应？（参考：0.2小，0.5中，0.8大）

---

### Step 6: 可视化对比（1小时）

```python
# 你的代码
# 任务：创建4个子图，对比Creative A和B的4个指标（箱线图或小提琴图）

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
metrics_display = ['ROAS', 'CPA', 'CTR', 'CVR']

for i, metric in enumerate(metrics):
    ax = axes[i//2, i%2]

    # 准备数据
    data = pd.DataFrame({
        metric: list(creative_a_stable[metric]) + list(creative_b_stable[metric]),
        'Creative': ['A'] * len(creative_a_stable) + ['B'] * len(creative_b_stable)
    })

    # 绘制箱线图
    sns.boxplot(data=data, x='Creative', y=metric, ax=ax)
    ax.set_title(f'{metrics_display[i]} Comparison')
    ax.set_ylabel(metrics_display[i])

plt.tight_layout()
plt.savefig('../output/figures/ab_test_comparison.png', dpi=300)
plt.show()
```

---

### Step 7: 生成测试报告（1小时）

```python
# 你的代码
# 任务：向Sarah生成一份测试报告，包含：
# - 测试设计（两个创意，测试时长，样本量）
# - 关键指标对比
# - t检验结果
# - 业务建议（是否推广Creative B）

report = f"""
# A/B测试报告 - Creative A vs Creative B

**测试日期**: 2024-03-01 至 2024-03-30
**测试平台**: Meta
**样本量**: Creative A {len(creative_a_stable)}天，Creative B {len(creative_b_stable)}天

## 测试结果

| 指标 | Creative A | Creative B | 差异 | p-value | 显著性 |
|------|-----------|-----------|-----|---------|--------|
| ROAS | ... | ... | ... | ... | Yes/No |
| CPA | ... | ... | ... | ... | Yes/No |
| CTR | ... | ... | ... | ... | Yes/No |
| CVR | ... | ... | ... | ... | Yes/No |

## 业务建议

### 🟢 推荐推广 / 🔴 不推荐推广

**理由**:
1. ...
2. ...

**风险**:
1. ...

**下一步**:
1. ...
"""

# 保存报告
with open('../output/reports/ab_test_report.md', 'w', encoding='utf-8') as f:
    f.write(report)

print("✅ 报告已保存到 output/reports/ab_test_report.md")
```

---

## 🎓 你将学到什么

通过Week 3，你将掌握：

### 预算优化
- ✅ 数学建模（目标函数、约束条件）
- ✅ 使用 scipy.optimize 求解优化问题
- ✅ 理解优化算法（SLSQP）
- ✅ 向业务方解释优化结果

### A/B测试
- ✅ 设计A/B测试（控制组 vs 实验组）
- ✅ 处理学习期数据
- ✅ t检验和p-value解释
- ✅ 效应量（Cohen's d）
- ✅ 统计显著性 vs 业务意义

### 业务沟通
- ✅ 生成专业的分析报告
- ✅ 用数据支持决策建议
- ✅ 讨论风险和局限性

---

## ✅ Week 3 完成标准

完成以下所有任务，Week 3就算完成：

1. ✅ 创建了 `notebooks/03_budget_optimization.ipynb`
2. ✅ 定义了目标函数和约束条件
3. ✅ 成功运行优化算法
4. ✅ 生成了预算优化报告（.md文件）
5. ✅ 创建了 `notebooks/04_ab_test_analysis.ipynb`
6. ✅ 完成了t检验分析
7. ✅ 生成了A/B测试报告（.md文件）
8. ✅ 生成了对比图表（.png文件）

---

## 🚀 下一步

完成Week 3后，告诉我：

**"Week 3完成了"**

然后我们开始：
- **Week 3（自动化ETL）**: 编写自动化脚本 + GitHub Actions
- **Week 4**: Power BI仪表盘 + 自动刷新演示

记住：**理解业务场景，不只是运行代码！**

---

**创建时间**: 2025-10-11
**目的**: 引导你学习统计分析方法，从优化到假设检验
