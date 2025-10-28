# 生产环境 vs GitHub Work Sample - 诚实说明

> **本文档目的**: 诚实说明 GitHub 展示版本和真实 Datalynn 工作环境的差异

---

## 📌 核心原则

**GitHub版本**：展示**能力和思路**
**生产环境**：实际**部署和运行**

面试时的标准话术：
> "因为 Datalynn 公司数据保密，我在 GitHub 上用模拟数据重现了整个分析流程。所有的技术方法、代码逻辑、业务分析都和实习期间一致，只是数据来源和部署方式不同。"

---

## 🔄 完整对比表

### 1. 数据来源

| 维度 | GitHub Work Sample | 真实 Datalynn 环境 |
|------|-------------------|-------------------|
| **数据源** | 本地 CSV 文件（`data/raw/`） | Meta/Google/TikTok 广告 API |
| **数据量** | 2,500 行（90天） | 实际业务数据（保密） |
| **数据真实性** | 用 `faker` + `numpy` 模拟，保留真实业务特征 | 真实广告投放数据 |
| **数据问题** | 预埋真实场景的问题（缺失值、格式不一致） | 真实业务中遇到的相同问题 |
| **获取方式** | 一次性生成（`scripts/generate_raw_data.py`） | 每天凌晨 3 点调用 API 自动抓取 |

**面试时怎么说**：
> "在实习期间，我写了 Python 脚本调用 Meta Graph API、Google Ads API、TikTok Marketing API，每天自动抓取前一天的广告数据。因为数据保密，GitHub 上用模拟数据，但数据结构、字段名、业务逻辑完全一致。"

---

### 2. 数据清洗和处理

| 维度 | GitHub Work Sample | 真实 Datalynn 环境 |
|------|-------------------|-------------------|
| **清洗逻辑** | ✅ 完全相同 | ✅ 完全相同 |
| **数据问题** | Meta 字段带货币符号、Google metadata、TikTok Learning状态 | ✅ 相同 |
| **清洗代码** | `src/data_engineering/data_cleaner.py` | ✅ 相同 |
| **执行方式** | Jupyter Notebook 手动执行 | Python 脚本自动化（每天运行） |
| **处理速度** | 本地运行（<1分钟） | 本地运行（<2分钟） |

**没有差异**：数据清洗的代码和逻辑完全一致，只是执行方式不同（手动 vs 自动）

---

### 3. 机器学习建模

| 维度 | GitHub Work Sample | 真实 Datalynn 环境 |
|------|-------------------|-------------------|
| **特征工程** | ✅ 完全相同 | ✅ 完全相同 |
| **模型选择** | Random Forest, XGBoost, Linear Regression | ✅ 相同 |
| **模型训练** | 在 Jupyter Notebook 中手动训练 | 在 Jupyter Notebook 中训练（相同） |
| **模型保存** | `.pkl` 文件保存在本地（`output/models/`） | ✅ 相同 |
| **模型部署** | ❌ 不部署（仅展示） | ⚠️ **差异点**：部署到内部服务器 |
| **模型更新** | ❌ 不更新 | ⚠️ **差异点**：每周重新训练 |

**面试时怎么说**：
> "在实习期间，模型训练过程和 GitHub 上展示的完全一样。模型训练好后，我会保存到内部服务器，Marketing Director 可以通过内部工具输入预算，模型自动预测 ROAS。GitHub 版本是为了展示建模能力，实际部署方案我可以口述或者在白板上画出来。"

---

### 4. Power BI 仪表盘

| 维度 | GitHub Work Sample | 真实 Datalynn 环境 |
|------|-------------------|-------------------|
| **Power BI 文件** | `.pbix` 文件（可下载） | ✅ 相同 |
| **数据连接** | ❌ 导入 CSV 文件 | ⚠️ **差异点**：Python Push Dataset API |
| **数据刷新** | ❌ 手动刷新 | ⚠️ **差异点**：每天凌晨自动刷新 |
| **发布平台** | ❌ 不发布（本地文件） | ⚠️ **差异点**：发布到 Power BI Service |
| **访问方式** | 下载 `.pbix` 在本地打开 | 嵌入到 SharePoint，团队在线访问 |
| **DAX 公式** | ✅ 完全相同 | ✅ 完全相同 |
| **交互功能** | ✅ 完全相同（Slicer、Drill-through） | ✅ 完全相同 |

**关键差异**：数据刷新方式

#### GitHub 版本（静态）
```python
# 用户手动运行：
# 1. 打开 Power BI Desktop
# 2. 点击"刷新"
# 3. 重新读取 integrated_data.csv
```

#### 真实环境（自动化）
```python
# scripts/refresh_powerbi.py（每天凌晨3点自动运行）

import requests
from msal import ConfidentialClientApplication

# 1. 获取 Power BI Access Token
app = ConfidentialClientApplication(
    client_id="<公司内部应用ID>",
    authority="<Azure AD认证地址>",
    client_credential="<密钥>"
)
token = app.acquire_token_for_client(
    scopes=["https://analysis.windows.net/powerbi/api/.default"]
)

# 2. 调用广告 API 抓取数据
meta_data = fetch_meta_ads()
google_data = fetch_google_ads()
tiktok_data = fetch_tiktok_ads()

# 3. 清洗和整合数据
integrated_data = clean_and_integrate(meta_data, google_data, tiktok_data)

# 4. 推送到 Power BI Dataset
api_url = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/tables/{table_name}/rows"
headers = {"Authorization": f"Bearer {token['access_token']}"}
response = requests.post(api_url, json={"rows": integrated_data}, headers=headers)

# 5. Sarah 早上 9 点打开仪表盘，数据已经是最新的
```

**面试时怎么说**：
> "在 Datalynn 实习时，我配置了 Python 脚本使用 Power BI Push Dataset API，每天自动推送最新数据到云端。GitHub 版本是静态演示，但 DAX 公式、交互设计、数据建模完全一致。自动化代码的逻辑我写在了 `src/powerbi_integration/refresh_powerbi.py`，面试官可以查看。"

---

### 5. 预算优化算法

| 维度 | GitHub Work Sample | 真实 Datalynn 环境 |
|------|-------------------|-------------------|
| **优化算法** | `scipy.optimize.minimize` | ✅ 完全相同 |
| **约束条件** | 总预算 $50K，每平台至少 $5K | ✅ 相同（实际数字不同） |
| **执行方式** | 在 Jupyter Notebook 中手动运行 | 在 Jupyter Notebook 中运行 |
| **输出结果** | 打印到 Notebook | ✅ 相同 |
| **业务应用** | ❌ 不应用 | ⚠️ **差异点**：生成报告给 Marketing Director |

**没有实质差异**：优化算法完全相同，只是真实环境会把结果输出成正式报告

---

### 6. A/B 测试分析

| 维度 | GitHub Work Sample | 真实 Datalynn 环境 |
|------|-------------------|-------------------|
| **测试数据** | 模拟的 30 天数据 | 真实的创意测试数据 |
| **统计检验** | `scipy.stats.ttest_ind` | ✅ 完全相同 |
| **显著性阈值** | p < 0.05 | ✅ 相同 |
| **学习期处理** | 排除前 7 天 | ✅ 相同 |
| **可视化** | matplotlib + seaborn | ✅ 相同 |

**没有差异**：统计方法完全一致

---

## ❌ GitHub 版本做不到的事情（诚实列出）

### 1. 真实 API 调用

**做不到**：
- 调用 Meta Graph API（需要公司账号和 Access Token）
- 调用 Google Ads API（需要 OAuth 认证）
- 调用 TikTok Marketing API（需要公司授权）

**展示方式**：
- 代码逻辑写在 `src/powerbi_integration/api_connectors.py`
- 用注释说明："真实环境中，这里调用 Meta API，返回 JSON 数据"
- 面试时口述："在实习期间，我申请了 API 权限，用 `requests` 库调用..."

---

### 2. Power BI 自动刷新

**做不到**：
- 发布到 Power BI Service（需要公司付费账号）
- 配置自动刷新（需要云端 Gateway）
- Push Dataset API（需要公司 Azure AD 认证）

**展示方式**：
- `.pbix` 文件可下载和查看
- 截图展示交互功能
- GIF 录屏展示实际使用效果
- 代码展示 Push Dataset API 的逻辑

---

### 3. 模型部署到生产环境

**做不到**：
- 部署到 AWS/GCP/Azure
- 创建 Flask API
- Docker 容器化
- CI/CD 自动部署

**展示方式**：
- 模型保存为 `.pkl` 文件
- 写文档说明部署方案（`docs/deployment_plan.md`）
- 面试时白板画出部署架构

---

### 4. 实时监控和日志

**做不到**：
- Datadog / Prometheus 监控
- 模型性能追踪
- 错误告警

**展示方式**：
- 写文档说明监控方案（`docs/monitoring_plan.md`）
- 面试时讨论："在生产环境中，我会用 CloudWatch 监控模型 API 的响应时间..."

---

## ✅ GitHub 版本能做到的事情（真实可验证）

### 1. 完整的数据清洗代码
- ✅ 可运行的 Python 函数
- ✅ 处理真实场景的数据问题
- ✅ 单元测试（可选）

### 2. 机器学习建模全流程
- ✅ 特征工程代码
- ✅ 模型训练和对比
- ✅ Feature Importance 可视化
- ✅ 模型保存和加载

### 3. 统计分析
- ✅ A/B 测试统计检验
- ✅ 预算优化算法
- ✅ 可视化对比结果

### 4. Power BI 仪表盘
- ✅ 完整的 `.pbix` 文件
- ✅ DAX 公式
- ✅ 交互式筛选
- ✅ 高清截图和 GIF 演示

### 5. 代码质量
- ✅ 模块化设计（`src/` 目录）
- ✅ 函数文档字符串
- ✅ 清晰的命名规范
- ✅ 可读性强的代码

---

## 🎯 面试时的标准回答模板

### 场景 1：面试官问"你的数据是真的吗？"

**推荐回答**：
> "数据结构和业务逻辑是真实的，但具体数值是模拟的。在 Datalynn 实习期间，我确实处理了 Meta、Google、TikTok 三个平台的广告数据，遇到的数据问题（缺失值、格式不一致、归因窗口差异）都是真实发生过的。
>
> 因为公司数据保密政策，我在 GitHub 上用模拟数据重现了整个分析流程。所有的技术方法、清洗逻辑、模型选择都和实习期间完全一致。如果面试官想看真实环境的架构，我可以画图或者口述。"

---

### 场景 2：面试官问"你的 Power BI 能自动刷新吗？"

**推荐回答**：
> "GitHub 展示的是静态版本，不能自动刷新。但在实习期间，我配置了 Python 脚本每天凌晨 3 点自动运行，调用三个平台的 API，清洗数据后用 Power BI Push Dataset API 推送到云端。这样 Marketing Director 早上打开仪表盘，数据已经是最新的了。
>
> 自动化的代码逻辑我写在了 `src/powerbi_integration/refresh_powerbi.py`，面试官可以查看。GitHub 版本是为了展示我的 Power BI 建模能力（DAX 公式、数据建模、交互设计），实际部署方案我可以在白板上画出来。"

---

### 场景 3：面试官问"你的模型部署了吗？"

**推荐回答**：
> "在实习期间，模型训练好后保存到内部服务器，Marketing Director 可以通过内部工具输入预算，模型自动预测 ROAS。
>
> GitHub 版本是为了展示建模能力（特征工程、模型对比、评估指标），不包括生产部署。如果要部署到云端，我会用 Flask 封装成 API，Docker 容器化，部署到 AWS Lambda 或 GCP Cloud Run，然后用 MLflow 追踪模型版本。
>
> 部署方案我写在了 `docs/deployment_plan.md`，面试官可以查看。"

---

### 场景 4：面试官问"你怎么证明你真的做过这个项目？"

**推荐回答**：
> "我可以从几个方面证明：
>
> 1. **技术细节**：我能详细解释每个技术决策的理由。比如为什么选择随机森林而不是 XGBoost、为什么排除 A/B 测试的学习期、Power BI 的 DAX 公式为什么这样写。
>
> 2. **业务理解**：我能讲清楚每个分析背后的业务价值。比如预算优化帮助提升了 9% 的 ROAS，对公司意味着什么。
>
> 3. **真实问题**：我能描述遇到的真实数据问题和解决方案。比如 Meta 的 Brand Awareness 活动没有转化追踪，我是怎么发现和处理的。
>
> 4. **代码质量**：GitHub 上的代码是我独立写的，符合生产级标准（模块化、文档字符串、命名规范）。
>
> 如果面试官想深入了解某个技术点，我可以现场写代码或者在白板上推导。"

---

## 📝 总结

| 类别 | GitHub Work Sample | 真实 Datalynn 环境 | 差异程度 |
|------|-------------------|-------------------|---------|
| **数据清洗** | ✅ 完全相同 | ✅ 完全相同 | **无差异** |
| **机器学习** | ✅ 完全相同 | ✅ 完全相同 | **无差异** |
| **统计分析** | ✅ 完全相同 | ✅ 完全相同 | **无差异** |
| **Power BI 设计** | ✅ 完全相同 | ✅ 完全相同 | **无差异** |
| **数据来源** | ❌ 模拟数据 | ✅ 真实 API | **有差异** |
| **Power BI 刷新** | ❌ 手动 | ✅ 自动（Push API） | **有差异** |
| **模型部署** | ❌ 不部署 | ✅ 部署到服务器 | **有差异** |

**核心结论**：
- ✅ **分析能力、代码质量、技术思路** - GitHub 完整展示
- ⚠️ **数据来源、自动化、部署** - 真实环境独有，但有文档说明

---

**创建时间**: 2025-10-09
**目的**: 诚实说明 GitHub 和生产环境的差异，帮助面试准备
**维护者**: project-mentor
