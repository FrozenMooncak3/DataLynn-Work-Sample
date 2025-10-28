# data 目录说明

仓库直接附带一份最新生成的模拟数据，方便面试官开箱即可运行代码：

- `raw/`：通过 `scripts/generate_raw_data.py` 生成的三平台原始导出（含预埋脏数据、隐私脱敏等问题）。
- `processed/`：Week 1 清洗流水线输出的统一指标表。
- `ab_test/`：Week 3 A/B 测试模拟数据。
- `DATA_DICTIONARY.md`：字段含义说明。

如需再生数据，可执行：

```bash
pip install -r requirements.txt
python scripts/generate_raw_data.py
python scripts/run_all_pipelines.py
```

脚本会自动覆盖上述目录中的 CSV，保证流程可复现。
