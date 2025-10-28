# 📊 Week 2: 机器学习建模（ROAS预测）

> 状态：草稿（等待 Week1 完成后补充实测笔记）

---

## ⚠️ 开始前必读

**在开始Week 2之前，请确认**：
- ✅ Week 1已完成（`data/processed/integrated_data.csv` 已生成）
- ✅ 已阅读 `ARCHITECTURE.md` 的Week 2部分
- ✅ Python环境已安装必要的库（见下方依赖清单）

---

## 🎯 本周学习目标

通过Week 2，你将学会：

1. **特征工程**：从原始数据创建预测特征
   - 滞后特征（Lag features）：过去7天的平均值
   - 时间特征（Time features）：星期几、是否周末
   - 分类编码（Categorical encoding）：平台one-hot编码

2. **模型训练和对比**：
   - 模型1：线性回归（Baseline）
   - 模型2：随机森林（Random Forest）
   - 模型3：XGBoost（梯度提升树）

3. **模型评估**：
   - MAE（Mean Absolute Error）：平均绝对误差
   - RMSE（Root Mean Squared Error）：均方根误差
   - R²（R-squared）：决定系数

4. **Feature Importance分析**：
   - 哪些特征对ROAS预测最重要？
   - 如何向业务方解释模型？

---

## 📦 依赖清单

在开始前，确保安装以下Python库：

```bash
pip install pandas numpy scikit-learn xgboost matplotlib seaborn
```

**版本要求**：
- pandas >= 2.0.3
- numpy >= 1.24.3
- scikit-learn >= 1.3.0
- xgboost >= 1.7.6
- matplotlib >= 3.7.2
- seaborn >= 0.12.2

---

## 🚀 Day 2-3 工作流程

### Day 2: 特征工程 + 模型训练（4-5小时）

```
08:00-09:00: 数据准备和探索性分析
09:00-11:00: 特征工程（滞后特征、时间特征）
11:00-12:00: 训练基准模型（线性回归）
12:00-13:00: 午休
13:00-15:00: 训练随机森林和XGBoost
15:00-16:00: 模型对比和评估
```

### Day 3: 模型优化 + Feature Importance（3-4小时）

```
08:00-10:00: 特征重要性分析
10:00-11:30: 模型调优（超参数调整）
11:30-12:00: 保存最佳模型
```

---

## 📝 Step 1: 数据准备和探索（30分钟）

### 创建新的Notebook

在 `notebooks/` 目录下创建 `02_roas_prediction.ipynb`

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 设置绘图风格
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# 读取Week 1清洗后的数据
df = pd.read_csv('../data/processed/integrated_data.csv')

print("数据概览:")
print(f"总行数: {len(df)}")
print(f"列名: {df.columns.tolist()}")
print(f"\n前5行:")
print(df.head())
```

### 探索性分析（你要做的）

**任务1**: 检查数据类型和缺失值

```python
# 你的代码
# 提示：使用 df.info() 和 df.isnull().sum()
```

**任务2**: 计算基本统计量

```python
# 你的代码
# 提示：使用 df.describe() 查看spend, ROAS等指标的分布
```

**任务3**: 可视化ROAS分布

```python
# 你的代码
# 提示：使用 plt.hist() 或 sns.histplot() 绘制ROAS直方图
```

**引导问题**：
- ❓ ROAS的平均值是多少？中位数是多少？
- ❓ 三个平台的ROAS分布有差异吗？
- ❓ 有没有异常值（如ROAS > 10或ROAS < 0）？

---

## 📝 Step 2: 特征工程（2-3小时）

### 2.1 转换日期列

首先，确保日期列是datetime类型：

```python
# 转换日期列
df['date'] = pd.to_datetime(df['date'])

# 按日期排序（重要！滞后特征需要顺序）
df = df.sort_values(['platform', 'date']).reset_index(drop=True)

print("日期范围:", df['date'].min(), "至", df['date'].max())
```

### 2.2 创建滞后特征（Lag Features）

**核心思想**: 使用过去7天的数据预测未来ROAS

```python
# 示例代码（你需要完成）
def create_lag_features(df, window=7):
    """
    创建滞后特征

    参数:
        df: 原始数据
        window: 滚动窗口大小（天数）

    返回:
        带滞后特征的数据
    """
    df_features = df.copy()

    # 按平台分组，计算过去7天的平均值
    for platform in ['Meta', 'Google', 'TikTok']:
        platform_data = df_features[df_features['platform'] == platform]

        # 滞后特征：过去7天的平均spend
        # 你的代码：使用 .rolling(window).mean()

        # 滞后特征：过去7天的平均ctr
        # 你的代码

        # 滞后特征：过去7天的平均cvr
        # 你的代码

        # 滞后特征：过去7天的平均cpa
        # 你的代码

    return df_features
```

**引导问题**：
- ❓ 为什么选择7天窗口？不是3天或14天？
- ❓ `.rolling(7).mean()` 的第1-6行会是什么？（提示：会有NaN）
- ❓ 如何处理这些NaN行？删除还是填充？

### 2.3 创建时间特征（Time Features）

```python
# 你的代码
# 任务1: 创建day_of_week特征（0=周一, 6=周日）
# 提示：使用 df['date'].dt.dayofweek

# 任务2: 创建is_weekend特征（0=工作日, 1=周末）
# 提示：day_of_week >= 5 即为周末

# 任务3: 创建month特征（1-12月）
# 提示：使用 df['date'].dt.month
```

### 2.4 分类编码（Categorical Encoding）

```python
# 任务：将platform列转换为one-hot编码
# 你的代码
# 提示：使用 pd.get_dummies(df, columns=['platform'])
```

**引导问题**：
- ❓ 为什么要做one-hot编码？模型不能直接用"Meta"、"Google"字符串吗？
- ❓ one-hot编码后会生成几列？
- ❓ 如果有100个不同的campaign_name，要不要也做one-hot？

### 2.5 选择最终特征和目标变量

```python
# 定义特征列（X）和目标列（y）
feature_columns = [
    'spend_last_7d',
    'ctr_last_7d',
    'cvr_last_7d',
    'cpa_last_7d',
    'day_of_week',
    'is_weekend',
    'month',
    'platform_Meta',
    'platform_Google',
    'platform_TikTok'
]

X = df_features[feature_columns]
y = df_features['roas']

print("特征矩阵形状:", X.shape)
print("目标变量形状:", y.shape)
print(f"\n删除NaN后行数: {X.dropna().shape[0]}")
```

---

## 📝 Step 3: 划分训练集和测试集（30分钟）

### 3.1 时间序列划分（重要！）

⚠️ **关键原则**: 广告数据是时间序列，不能随机划分！

```python
from sklearn.model_selection import train_test_split

# ❌ 错误做法（随机划分）
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ 正确做法（时间划分）
# 前80%作为训练集，后20%作为测试集
split_index = int(len(X) * 0.8)

X_train = X[:split_index]
X_test = X[split_index:]
y_train = y[:split_index]
y_test = y[split_index:]

print(f"训练集: {len(X_train)}行")
print(f"测试集: {len(X_test)}行")
print(f"训练集日期范围: {df.loc[X_train.index, 'date'].min()} 至 {df.loc[X_train.index, 'date'].max()}")
print(f"测试集日期范围: {df.loc[X_test.index, 'date'].min()} 至 {df.loc[X_test.index, 'date'].max()}")
```

**引导问题**：
- ❓ 为什么不能随机划分时间序列数据？
- ❓ 如果随机划分，会导致什么问题？（提示：用未来数据预测过去）
- ❓ 80/20划分是固定的吗？可以改成70/30吗？

---

## 📝 Step 4: 训练基准模型（线性回归）（30分钟）

### 4.1 训练线性回归

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 训练模型
lr = LinearRegression()
lr.fit(X_train, y_train)

# 预测
lr_pred = lr.predict(X_test)

# 评估
lr_mae = mean_absolute_error(y_test, lr_pred)
lr_rmse = np.sqrt(mean_squared_error(y_test, lr_pred))
lr_r2 = r2_score(y_test, lr_pred)

print("线性回归模型评估:")
print(f"MAE: {lr_mae:.4f}")
print(f"RMSE: {lr_rmse:.4f}")
print(f"R²: {lr_r2:.4f}")
```

### 4.2 可视化预测结果

```python
# 你的代码
# 任务：绘制散点图，横轴是真实ROAS，纵轴是预测ROAS
# 提示：使用 plt.scatter(y_test, lr_pred)
# 添加对角线（y=x），表示完美预测
# 提示：plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
```

**引导问题**：
- ❓ MAE=0.52是什么意思？（提示：平均预测误差0.52美元ROAS）
- ❓ R²=0.65是好还是坏？（提示：65%的方差被解释）
- ❓ 为什么散点图中有些点离对角线很远？

---

## 📝 Step 5: 训练随机森林（2小时）

### 5.1 训练随机森林模型

```python
from sklearn.ensemble import RandomForestRegressor

# 训练模型
rf = RandomForestRegressor(
    n_estimators=100,      # 100棵树
    max_depth=10,          # 最大深度10
    min_samples_split=5,   # 节点最小样本数5
    random_state=42
)

rf.fit(X_train, y_train)

# 预测
rf_pred = rf.predict(X_test)

# 评估
rf_mae = mean_absolute_error(y_test, rf_pred)
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
rf_r2 = r2_score(y_test, rf_pred)

print("随机森林模型评估:")
print(f"MAE: {rf_mae:.4f}")
print(f"RMSE: {rf_rmse:.4f}")
print(f"R²: {rf_r2:.4f}")
```

### 5.2 Feature Importance分析

```python
# 提取特征重要性
feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

print("特征重要性排名:")
print(feature_importance)

# 可视化
plt.figure(figsize=(10, 6))
plt.barh(feature_importance['feature'][:10], feature_importance['importance'][:10])
plt.xlabel('Importance')
plt.title('Top 10 Feature Importance (Random Forest)')
plt.tight_layout()
plt.savefig('../output/figures/feature_importance.png', dpi=300)
plt.show()
```

**引导问题**：
- ❓ 哪个特征最重要？为什么？
- ❓ 时间特征（is_weekend）重要吗？
- ❓ 三个平台的one-hot特征重要性有差异吗？

---

## 📝 Step 6: 训练XGBoost（1小时）

### 6.1 训练XGBoost模型

```python
from xgboost import XGBRegressor

# 训练模型
xgb = XGBRegressor(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    random_state=42
)

xgb.fit(X_train, y_train)

# 预测
xgb_pred = xgb.predict(X_test)

# 评估
xgb_mae = mean_absolute_error(y_test, xgb_pred)
xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_pred))
xgb_r2 = r2_score(y_test, xgb_pred)

print("XGBoost模型评估:")
print(f"MAE: {xgb_mae:.4f}")
print(f"RMSE: {xgb_rmse:.4f}")
print(f"R²: {xgb_r2:.4f}")
```

---

## 📝 Step 7: 模型对比和选择（1小时）

### 7.1 对比三个模型

```python
# 你的代码
# 任务：创建一个DataFrame，对比三个模型的MAE、RMSE、R²
# 提示：
results = pd.DataFrame({
    'Model': ['Linear Regression', 'Random Forest', 'XGBoost'],
    'MAE': [lr_mae, rf_mae, xgb_mae],
    'RMSE': [lr_rmse, rf_rmse, xgb_rmse],
    'R²': [lr_r2, rf_r2, xgb_r2]
})

print(results)
```

### 7.2 可视化对比

```python
# 你的代码
# 任务：绘制柱状图，对比三个模型的MAE
# 提示：
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# 子图1：MAE对比
axes[0].bar(results['Model'], results['MAE'])
axes[0].set_title('MAE Comparison')
axes[0].set_ylabel('MAE')

# 子图2：RMSE对比
# 你的代码

# 子图3：R²对比
# 你的代码

plt.tight_layout()
plt.savefig('../output/figures/model_comparison.png', dpi=300)
plt.show()
```

### 7.3 选择最佳模型

**决策原则**：
1. **首先看MAE**（最直观的误差指标）
2. **考虑R²**（解释能力）
3. **考虑训练时间**（生产环境重要）
4. **考虑可解释性**（向业务方解释）

**引导问题**：
- ❓ 哪个模型的MAE最低？
- ❓ 如果XGBoost的MAE比随机森林低0.03，但训练时间多3倍，你会选哪个？
- ❓ 如何向Marketing Director解释"为什么选择这个模型"？

---

## 📝 Step 8: 保存模型和结果（30分钟）

### 8.1 保存最佳模型

```python
import pickle

# 假设选择随机森林作为最佳模型
best_model = rf
best_model_name = 'random_forest'

# 保存模型
with open(f'../output/models/{best_model_name}_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)

print(f"✅ 模型已保存到 output/models/{best_model_name}_model.pkl")
```

### 8.2 保存模型评估指标

```python
import json

# 保存指标
metrics = {
    'model_name': best_model_name,
    'mae': float(rf_mae),
    'rmse': float(rf_rmse),
    'r2': float(rf_r2),
    'train_size': len(X_train),
    'test_size': len(X_test),
    'feature_columns': feature_columns,
    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

with open('../output/models/model_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)

print("✅ 模型指标已保存到 output/models/model_metrics.json")
```

### 8.3 生成模型报告

```python
# 你的代码
# 任务：在notebook末尾添加一个Markdown单元格，总结：
# - 最佳模型是什么
# - MAE/RMSE/R²指标
# - 前5个最重要的特征
# - 模型的局限性（如数据量小、时间范围短）
# - 未来改进方向（如增加更多特征、调优超参数）
```

---

## 🎓 你将学到什么

通过Week 2，你将掌握：

### 技术能力
- ✅ 特征工程（滞后特征、时间特征、分类编码）
- ✅ 时间序列划分（不能随机！）
- ✅ 训练多个模型（线性回归、随机森林、XGBoost）
- ✅ 模型评估（MAE、RMSE、R²）
- ✅ Feature Importance分析
- ✅ 模型持久化（pickle）

### 业务理解
- ✅ 为什么ROAS预测重要？（预算规划、效果评估）
- ✅ 如何选择模型？（准确性 vs 速度 vs 可解释性）
- ✅ 如何向非技术人员解释模型？

### 面试准备
- ✅ 能流畅讲述模型训练过程
- ✅ 能解释为什么选择这个模型
- ✅ 能回答"MAE=0.42是好还是坏"
- ✅ 能讨论模型的局限性和改进方向

---

## ✅ Week 2 完成标准

完成以下所有任务，Week 2就算完成：

1. ✅ 创建了 `notebooks/02_roas_prediction.ipynb`
2. ✅ 完成了特征工程（滞后特征 + 时间特征）
3. ✅ 训练了3个模型（线性回归、随机森林、XGBoost）
4. ✅ 生成了模型对比图表
5. ✅ 分析了Feature Importance
6. ✅ 保存了最佳模型（.pkl文件）
7. ✅ 保存了模型指标（.json文件）
8. ✅ 生成了高质量的图表（feature_importance.png, model_comparison.png）

---

## 🚀 下一步

完成Week 2后，告诉我：

**"Week 2完成了"**

然后我们开始：
- **Week 2（下半部分）**: 预算优化（使用训练好的模型）
- **Week 3**: A/B测试分析 + 自动化ETL

记住：**不要急着写代码，先理解原理！**

---

**创建时间**: 2025-10-11
**目的**: 引导你一步步学习机器学习建模，从特征工程到模型评估
