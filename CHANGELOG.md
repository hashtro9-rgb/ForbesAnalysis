# Changelog

All notable changes to this project are documented in this file.

## [1.1.0] — 2026-07-03

### Added
- Insights & Recommendations panel — auto-generated, recalculated live from whatever subset of companies is currently filtered (market concentration, geographic share, margin split, plus three plain-language recommendations)
- `tests/test_data_quality.py` — automated checks against the cleaned dataset
- `notebooks/exploratory_analysis.ipynb` — exploratory analysis notebook
- Repository restructured into a standard portfolio layout (`data/`, `dashboard/`, `docs/`, `scripts/`, `tests/`, `notebooks/`)
- GitHub Actions workflow for automatic Pages deployment on push to `main`

### Changed
- Dashboard rebuilt from an editorial/magazine layout into a BI-tool style layout: sidebar navigation, KPI row, live filters panel, chart grid, company explorer table
- Locked visual design to a single "Trading Floor" palette (near-black background, gold accent, green/red profitability coding) instead of a multi-theme switcher
- Fixed a filtering bug where KPIs, charts, the country breakdown, and the leaderboard did not respond to filter changes — only the table did. All dashboard sections now update together through a single `updateAll()` pass
- Split the dashboard into `index.html`, `style.css`, and `script.js` for maintainability
- Dataset embedded directly in the dashboard as inline JSON — removes the CSV fetch dependency, so the dashboard runs standalone with no server

### Fixed
- `Uncaught ReferenceError: Cannot access 'charts' before initialization` — moved variable declaration ahead of first use

## [1.0.0] — 2026-07-02

### Added
- Initial data cleaning pipeline (`clean_forbes_2000.py`) — missing value handling, city/country extraction, derived financial metrics (Profit Margin %, Asset Efficiency, ROA %)
- Data quality report generation
- First version of the interactive dashboard (editorial/magazine style, three color themes: Boardroom, Trading Floor, Broadsheet)
- Project README and portfolio documentation
