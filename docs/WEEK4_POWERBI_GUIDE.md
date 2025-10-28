# 📊 Week 4: Power BI仪表盘 + 自动刷新演示

> 状态：草稿（待数据建模完成后扩写可视化步骤）

---

## ⚠️ 开始前必读

**在开始Week 4之前，请确认**：
- ✅ Week 1-3已完成（所有数据清洗、建模、分析已完成）
- ✅ 已安装 Power BI Desktop（免费版）
- ✅ `data/processed/integrated_data.csv` 已生成
- ✅ 已阅读 `ARCHITECTURE.md` 的Week 3-4部分

---

## 🎯 本周学习目标

通过Week 4，你将学会：

### Part 1: Power BI仪表盘设计
- 导入CSV数据到Power BI
- 创建日期维度表
- 编写DAX公式计算指标
- 设计3页交互式仪表盘：
  - Page 1: Overview（KPI卡片 + 趋势图）
  - Page 2: Platform Comparison（柱状图 + 散点图）
  - Page 3: Time Analysis（日历热力图 + 瀑布图）

### Part 2: 自动刷新演示（GitHub版）
- 配置GitHub Actions每日运行ETL
- 演示"数据自动更新"流程
- 录制演示GIF（模拟自动刷新）
- 诚实说明GitHub vs 生产环境差异

---

## 📦 软件安装

### Power BI Desktop

**下载地址**: https://www.microsoft.com/zh-cn/power-platform/products/power-bi/desktop

**版本**: 免费版（无需订阅）

**安装后确认**: 打开Power BI Desktop → "获取数据" → 看到"文本/CSV"选项即可

---

## 🚀 Day 6 工作流程（6-8小时）

```
08:00-10:00: 导入数据 + 创建维度表
10:00-12:00: 编写DAX公式 + Page 1设计
12:00-13:00: 午休
13:00-15:00: Page 2 + Page 3 设计
15:00-16:00: 美化和交互设计
16:00-17:00: 截图 + 录制GIF
17:00-18:00: 配置GitHub Actions（自动刷新演示）
```

---

## 📝 Part 1: 导入数据和数据建模

### Step 1: 导入CSV数据（30分钟）

#### 打开Power BI Desktop

1. 点击"获取数据" → "文本/CSV"
2. 选择 `data/processed/integrated_data.csv`
3. 预览数据，确认列名正确
4. 点击"加载"

**检查数据类型**：
- `date`: 日期类型
- `spend`, `impressions`, `clicks`, `conversions`, `revenue`: 整数或小数
- `ctr`, `cvr`, `cpa`, `roas`: 小数
- `platform`, `campaign_name`: 文本

**任务**：如果数据类型不对，点击"转换数据" → 更改类型

---

### Step 2: 创建日期维度表（30分钟）

**为什么需要日期维度表？**
- Power BI的时间智能函数需要独立的日期表
- 可以添加年、季度、月、周等派生列
- 便于时间切片和筛选

#### 创建日期表

在Power BI中，点击"新建表"，输入以下DAX公式：

```dax
DateTable =
CALENDAR(
    MIN(integrated_data[date]),
    MAX(integrated_data[date])
)
```

#### 添加派生列

点击DateTable表 → "新建列"，依次添加：

```dax
Year = YEAR(DateTable[Date])

Quarter = "Q" & FORMAT(DateTable[Date], "Q")

Month = FORMAT(DateTable[Date], "MMMM")

MonthNum = MONTH(DateTable[Date])

DayOfWeek = FORMAT(DateTable[Date], "dddd")

IsWeekend = IF(WEEKDAY(DateTable[Date], 2) >= 6, "Weekend", "Weekday")
```

#### 建立关系

1. 点击左侧"模型视图"（三个表的图标）
2. 将 `DateTable[Date]` 拖到 `integrated_data[date]`
3. 确认关系类型为"一对多"

---

### Step 3: 创建度量值（Measures）（1小时）

**什么是度量值？**
- 度量值是动态计算的指标，会根据筛选器自动聚合
- 例如：总spend、平均ROAS、ROAS同比增长

#### 创建度量值文件夹

在 `integrated_data` 表中，右键 → "新建组" → 命名为 "Measures"

#### 创建基础度量值

依次创建以下度量值（右键Measures → "新建度量值"）：

```dax
Total Spend = SUM(integrated_data[spend])

Total Impressions = SUM(integrated_data[impressions])

Total Clicks = SUM(integrated_data[clicks])

Total Conversions = SUM(integrated_data[conversions])

Total Revenue = SUM(integrated_data[revenue])

Average ROAS = AVERAGE(integrated_data[roas])

Average CPA = AVERAGE(integrated_data[cpa])

Average CTR = AVERAGE(integrated_data[ctr])

Average CVR = AVERAGE(integrated_data[cvr])
```

#### 创建高级度量值

```dax
ROAS (Calculated) =
DIVIDE([Total Revenue], [Total Spend], 0)

CTR (Calculated) =
DIVIDE([Total Clicks], [Total Impressions], 0)

CVR (Calculated) =
DIVIDE([Total Conversions], [Total Clicks], 0)

CPA (Calculated) =
DIVIDE([Total Spend], [Total Conversions], 0)
```

**引导问题**：
- ❓ `Average ROAS` 和 `ROAS (Calculated)` 有什么区别？
- ❓ 为什么用 `DIVIDE()` 而不是 `/` ？（提示：避免除零错误）

---

## 📝 Part 2: 设计仪表盘（3-4小时）

### Page 1: Overview（总览页）

**目标**: 展示整体表现和趋势

#### 布局设计

```
+---------------------------------------+
|  Total Spend  |  Total Revenue  | ROAS |
+---------------------------------------+
|   ROAS Trend (折线图)                 |
+---------------------------------------+
|   Platform Performance (柱状图)       |
+---------------------------------------+
```

#### 添加KPI卡片

1. **Total Spend卡片**：
   - 点击"卡片"可视化
   - 拖入 `[Total Spend]` 度量值
   - 格式：货币格式（$）

2. **Total Revenue卡片**：
   - 同上，拖入 `[Total Revenue]`

3. **ROAS卡片**：
   - 拖入 `[ROAS (Calculated)]`
   - 格式：小数点后2位

**任务**：美化卡片
- 调整背景色（浅蓝色、浅绿色）
- 增大字体（48pt）
- 添加数据标签

#### 添加ROAS趋势图

1. 点击"折线图"可视化
2. X轴：`DateTable[Date]`
3. Y轴：`[ROAS (Calculated)]`
4. 图例：`platform`（显示三条线）

**美化**：
- 启用"数据标签"
- 设置颜色主题（Meta=蓝色，Google=绿色，TikTok=黑色）
- 添加网格线

#### 添加平台表现对比图

1. 点击"簇状柱形图"
2. X轴：`platform`
3. Y轴：`[Total Spend]`, `[Total Revenue]`

**引导问题**：
- ❓ 三个平台哪个ROAS最高？
- ❓ ROAS趋势是上升还是下降？
- ❓ 如何添加日期筛选器？（提示：拖入 `DateTable[Date]` 到"筛选器"面板）

---

### Page 2: Platform Comparison（平台对比）

**目标**: 深入对比三个平台的表现

#### 布局设计

```
+---------------------------------------+
|   Spend vs Revenue (散点图)            |
+---------------------------------------+
|   CPA vs ROAS (散点图)                 |
+---------------------------------------+
|   Platform Metrics Table (表格)       |
+---------------------------------------+
```

#### 添加Spend vs Revenue散点图

1. 点击"散点图"
2. X轴：`[Total Spend]`
3. Y轴：`[Total Revenue]`
4. 图例：`platform`
5. 大小：`[Total Impressions]`（气泡大小）

**解读**：
- 越靠右上角的平台越好（高收入、高投入）
- 气泡越大说明曝光量越大

#### 添加CPA vs ROAS散点图

1. 点击"散点图"
2. X轴：`[Average CPA]`
3. Y轴：`[Average ROAS]`
4. 图例：`platform`

**解读**：
- 左上角最优（低CPA、高ROAS）
- 右下角最差（高CPA、低ROAS）

#### 添加平台指标表

1. 点击"表格"
2. 列：
   - `platform`
   - `[Total Spend]`
   - `[Total Revenue]`
   - `[ROAS (Calculated)]`
   - `[Average CPA]`
   - `[Average CTR]`
   - `[Average CVR]`

**美化**：
- 条件格式：ROAS > 3.0 显示绿色，< 2.0 显示红色
- 排序：按ROAS降序

---

### Page 3: Time Analysis（时间分析）

**目标**: 发现时间模式（周几效果好、月度趋势）

#### 布局设计

```
+---------------------------------------+
|   ROAS by Day of Week (柱状图)         |
+---------------------------------------+
|   Monthly Trend (瀑布图)               |
+---------------------------------------+
|   Heatmap (矩阵)                       |
+---------------------------------------+
```

#### 添加"周几效果"柱状图

1. 点击"柱形图"
2. X轴：`DateTable[DayOfWeek]`
3. Y轴：`[Average ROAS]`

**排序**：
- 自定义排序（周一到周日）
- 点击图表 → "..."菜单 → "按DayOfWeek排序"

**引导问题**：
- ❓ 周末的ROAS比工作日高还是低？
- ❓ 这个发现对预算分配有什么启示？

#### 添加月度瀑布图

1. 点击"瀑布图"
2. 类别：`DateTable[Month]`
3. Y轴：`[Total Revenue]`

**解读**：
- 瀑布图显示月度收入的增减变化
- 可以看到哪个月是"跳水"还是"飙升"

#### 添加热力图（矩阵）

1. 点击"矩阵"
2. 行：`DateTable[DayOfWeek]`
3. 列：`platform`
4. 值：`[Average ROAS]`

**美化**：
- 条件格式 → 背景色 → 渐变色（低ROAS=红色，高ROAS=绿色）

**解读**：
- 可以看到"Meta在周末表现最好"等模式

---

## 📝 Part 3: 交互设计（1小时）

### 添加筛选器

在每一页添加以下筛选器（在右侧"筛选器"面板）：

1. **日期范围筛选器**：
   - 拖入 `DateTable[Date]`
   - 筛选类型："相对日期"或"日期范围"

2. **平台筛选器**：
   - 拖入 `platform`
   - 筛选类型："基本筛选"（复选框）

3. **ROAS阈值筛选器**：
   - 拖入 `[Average ROAS]`
   - 筛选类型："高级筛选" → "大于" 2.0

### 添加切片器（Slicer）

1. 点击"切片器"可视化
2. 拖入 `platform`
3. 样式：水平排列的按钮

**测试交互**：
- 点击"Meta" → 所有图表自动筛选只显示Meta数据
- 点击"清除筛选" → 恢复全部数据

---

## 📝 Part 4: 保存和导出（30分钟）

### 保存.pbix文件

1. 点击"文件" → "另存为"
2. 保存到 `powerbi/datalynn_dashboard.pbix`

### 导出截图

**每一页导出高清截图**：
1. 点击页面
2. 按 `Ctrl + Shift + S`（或"文件" → "导出" → "导出为图片"）
3. 保存到 `powerbi/screenshots/`

**文件命名**：
- `01_overview.png`
- `02_platform_comparison.png`
- `03_time_analysis.png`

---

## 📝 Part 5: 录制演示GIF（1小时）

### 使用Windows自带的屏幕录制

1. 打开Power BI Desktop
2. 按 `Win + G` 打开Xbox Game Bar
3. 点击"录制"按钮（圆形图标）
4. 演示以下操作：
   - 切换不同页面
   - 拖动日期切片器
   - 点击平台筛选器
   - 数据自动更新的动画效果
5. 停止录制（保存为.mp4）

### 转换为GIF

1. 访问 https://ezgif.com/video-to-gif
2. 上传.mp4文件
3. 调整大小（建议800px宽度）
4. 生成GIF
5. 保存到 `powerbi/demo.gif`

**时长建议**: 15-20秒（太长文件会很大）

---

## 📝 Part 6: 自动刷新演示（GitHub版）（2-3小时）

### 策略说明

**GitHub限制**：
- GitHub是静态托管，无法运行Power BI Service
- 无法实现真正的"自动刷新"（需要Power BI Service云端）

**解决方案**：
- 用GitHub Actions每天更新CSV数据
- 用户下载.pbix → 手动点击"刷新" → 数据自动从最新CSV加载
- 在README中诚实说明"这是模拟演示"

---

### Step 1: 创建自动化ETL脚本（30分钟）

**文件路径**: `scripts/daily_etl.py`

（此脚本已在 `ARCHITECTURE.md` 的Week 3部分定义，你需要实际创建这个文件）

**关键点**：
- 每天生成新的 `integrated_data.csv`
- 保存时间戳版本（如 `integrated_data_20250411.csv`）
- 同时更新最新版本 `integrated_data.csv`

---

### Step 2: 配置GitHub Actions（1小时）

**文件路径**: `.github/workflows/daily_etl.yml`

（配置内容已在 `ARCHITECTURE.md` 定义）

**测试流程**：
1. 提交代码到GitHub
2. 前往GitHub仓库 → "Actions"标签
3. 手动触发工作流（"Run workflow"按钮）
4. 查看运行日志，确认CSV更新成功

---

### Step 3: 演示自动刷新（30分钟）

#### 录制演示视频

**脚本**：
1. 打开GitHub仓库 → "Actions"标签
2. 展示最近的ETL运行记录（✅成功）
3. 点击某次运行 → 展示日志（"整合数据已保存"）
4. 打开Power BI Desktop
5. 打开 `datalynn_dashboard.pbix`
6. 点击"主页" → "刷新"按钮
7. 数据自动更新（日期范围变化）
8. 展示"数据已更新到最新日期"

**保存为GIF**：
- 上传到 `powerbi/auto_refresh_demo.gif`

---

### Step 4: 创建说明文档（30分钟）

**文件路径**: `docs/powerbi_auto_refresh.md`

```markdown
# Power BI 自动刷新说明

## GitHub演示版本

### 自动化流程

1. **GitHub Actions每天凌晨2点运行**：
   - 执行 `scripts/daily_etl.py`
   - 清洗最新数据
   - 更新 `data/processed/integrated_data.csv`
   - 自动commit到GitHub

2. **用户手动刷新Power BI**：
   - 下载最新的 `.pbix` 文件
   - 打开Power BI Desktop
   - 点击"刷新"按钮
   - 数据自动从最新CSV加载

### 演示GIF

![自动刷新演示](../powerbi/auto_refresh_demo.gif)

---

## 真实生产环境（Datalynn实习期间）

### 自动化流程

1. **Python脚本每天凌晨3点运行**：
   - 调用Meta Marketing API
   - 调用Google Ads API
   - 调用TikTok Ads API
   - 清洗和整合数据
   - 使用Power BI Push Dataset API推送到云端

2. **Power BI Service自动刷新**：
   - Sarah打开Power BI Service（网页端）
   - 数据已自动更新（无需手动刷新）

### 技术栈

- **调度**: Airflow DAG
- **API调用**: Python `requests` 库
- **数据推送**: Power BI REST API
- **监控**: 失败时发送邮件告警

### 代码示例

（伪代码，展示真实实现的逻辑）

```python
import requests

# 推送数据到Power BI Service
def push_to_powerbi(df, dataset_id, table_name):
    url = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/tables/{table_name}/rows"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = df.to_dict(orient='records')
    response = requests.post(url, json={"rows": data}, headers=headers)
    return response
```

---

## 面试时如何解释

**问题**: "你的仪表盘能自动刷新吗？"

**回答**:
> "在GitHub上展示的是模拟版本，因为：
> 1. 数据是模拟的CSV（公司数据保密）
> 2. Power BI自动刷新需要Power BI Service（付费云端账号）
>
> 在Datalynn实习时，我配置了Python脚本每天自动调用API、清洗数据、推送到Power BI云端。Sarah早上打开仪表盘，数据已经是最新的了。
>
> GitHub版本展示的是我的分析能力和代码质量，真实环境的自动化逻辑我写在了`docs/powerbi_auto_refresh.md`，面试官可以查看。"
```

---

## 🎓 你将学到什么

通过Week 4，你将掌握：

### Power BI技能
- ✅ 导入CSV数据
- ✅ 创建日期维度表
- ✅ 编写DAX公式（SUM, AVERAGE, DIVIDE）
- ✅ 设计3页交互式仪表盘
- ✅ 使用切片器和筛选器
- ✅ 条件格式和可视化美化

### 自动化演示
- ✅ 配置GitHub Actions
- ✅ 录制演示GIF
- ✅ 诚实说明GitHub vs 生产环境差异

### 面试准备
- ✅ 能流畅演示仪表盘功能
- ✅ 能解释自动刷新的实现原理
- ✅ 能诚实回答"GitHub版本的局限性"

---

## ✅ Week 4 完成标准

完成以下所有任务，Week 4就算完成：

1. ✅ 创建了 `powerbi/datalynn_dashboard.pbix`
2. ✅ 设计了3页仪表盘（Overview, Platform Comparison, Time Analysis）
3. ✅ 编写了10+个DAX度量值
4. ✅ 导出了3-5张高清截图
5. ✅ 录制了交互演示GIF
6. ✅ 配置了GitHub Actions自动ETL
7. ✅ 创建了 `docs/powerbi_auto_refresh.md` 说明文档
8. ✅ 录制了自动刷新演示GIF

---

## 🚀 下一步

完成Week 4后，告诉我：

**"Week 4完成了"**

然后我们开始：
- **Week 4（收尾）**: 完善README，准备面试问答
- **最终检查**: 确保所有文件完整、GitHub整洁

恭喜你！DataLynn项目即将完成！🎉

---

**创建时间**: 2025-10-11
**目的**: 引导你完成Power BI仪表盘设计和自动刷新演示
