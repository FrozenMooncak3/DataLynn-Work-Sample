# Power BI Deliverable

This project expects a Power BI dashboard to live in `datalynn_dashboard.pbix` once you finish designing the visuals.

Suggested workflow:

1. Run `python scripts/run_all_pipelines.py` to refresh `data/processed/integrated_data.csv` and Week 3 reports.
2. In Power BI Desktop choose **Get Data → Text/CSV** and point to the CSV above (or connect to the entire `data/processed/` folder).
3. Recreate the measures described in `docs/WEEK4_POWERBI_GUIDE.md` and save the report as `powerbi/datalynn_dashboard.pbix`.
4. Export static screenshots to `powerbi/screenshots/` and (optionally) record an animated GIF demo in `powerbi/demo.gif`.

_Why the PBIX is not committed yet:_ The repository keeps the workflow reproducible without large binaries. Use this folder as the canonical location when you produce the final dashboard.
