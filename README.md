<p align="center">
  <img src="assets/images/banner.png" alt="Forbes Global 2000 Analytics Dashboard" width="100%">
</p>

# Forbes Global 2000 (2026) — Analytics Dashboard

**Portfolio Project** | Data Analytics | Interactive BI Dashboard | CI/CD → GitHub Pages

An end-to-end analytics project on the world's 2,000 largest public companies: a documented Python cleaning pipeline, automated data-quality tests, an exploratory analysis notebook, and a self-contained interactive dashboard with live filters and computed insights.

🔗 **Live Dashboard:** *(GitHub Pages URL after deployment)*

---

## 📸 Preview

<!-- TODO: replace with real captures once deployed
![Dashboard Overview](assets/images/dashboard-overview.png)
![Demo](assets/gifs/dashboard-demo.gif)
-->

*Screenshots and demo GIF coming after first deployment — see `assets/`.*

---

## 🗂 Repository Structure

```
ForbesAnalysis/
├── .github/workflows/deploy.yml   # Auto-deploys dashboard/ to GitHub Pages on push
├── assets/                        # Banner, screenshots, demo GIF
├── dashboard/                     # index.html + style.css + script.js (data embedded)
├── data/
│   ├── raw/                       # Original Kaggle export (2000 × 8)
│   ├── processed/                 # Cleaned dataset (2000 × 12)
│   └── reports/                   # Generated data quality report
├── docs/
│   ├── Project_Report.pdf         # Full project write-up
│   ├── Data_Dictionary.pdf        # Column-by-column schema reference
│   ├── Dashboard_Guide.pdf        # User guide for every dashboard feature
│   └── Architecture.png           # Pipeline diagram
├── notebooks/
│   └── exploratory_analysis.ipynb # EDA — executed and verified error-free
├── scripts/
│   └── clean_forbes_2000.py       # Cleaning pipeline (raw → processed + report)
├── tests/
│   └── test_data_quality.py       # 12 pytest checks on the cleaned dataset
├── requirements.txt
├── CHANGELOG.md
├── LICENSE                        # MIT (code only — dataset has its own terms)
└── README.md
```

---

## 🔧 The Pipeline

```
raw CSV ──► clean_forbes_2000.py ──► cleaned CSV + quality report
                                          │
                              pytest (12 checks) ✅
                                          │
                          embedded as JSON in dashboard/script.js
                                          │
                     push to main ──► GitHub Actions ──► GitHub Pages
```

**Cleaning highlights:**
- Split `Headquarters` → `City` + `Country` (62 countries) — including an edge case where one company listed only a country, caught by the test suite and fixed at the source
- Filled 1 missing `Industry` (business-profile judgment); left 1 missing `Market Value` as an honest null rather than fabricating a number
- Engineered `Profit_Margin_%`, `Asset_Efficiency`, and `ROA_%` from source columns only

**Test suite:** 12 automated checks — row counts, schema, duplicates, value ranges, null bounds, junk-string detection, and a numerical spot-check that recomputes Profit Margin from source columns. **12/12 passing.**

---

## 📊 The Dashboard

BI-tool layout in a single deployable folder — sidebar navigation, KPI row, sticky filters panel, linked chart grid, computed insights, and a sortable company explorer.

| Feature | Detail |
|---|---|
| **Live filters** | Country · Industry · Rank Range · Profitability tier · name search — every chart, KPI, insight, and table updates together |
| **Charts** | Market value by rank tier, industry donut, country heat-grid, top-10 leaderboard, industry bars, margin histogram, ROA by tier |
| **Insights engine** | Concentration, geographic exposure, and margin-split narratives recomputed from whatever subset is filtered — with threshold-based recommendations |
| **Design** | "Trading Floor" palette — near-black, gold accent, green/red ticker coding on profitability figures |
| **Zero dependencies at runtime** | Dataset embedded as inline JSON — no fetch, no CORS issues, works opened directly from disk |

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Re-run the cleaning pipeline (optional — outputs are committed)
cd scripts && python3 clean_forbes_2000.py

# 3. Run the data quality tests
pytest tests/test_data_quality.py -v

# 4. Open the dashboard — no server needed
open dashboard/index.html        # macOS
start dashboard\index.html       # Windows
```

**Deploying:** push to `main` — the GitHub Actions workflow publishes `dashboard/` to GitHub Pages automatically (enable Pages → Source: GitHub Actions in repo settings first).

---

## 🔍 Key Findings

- **US dominance:** 595 of 2,000 companies (29.8%); US + China + Japan = over half the list
- **Banking everywhere:** largest industry by count (314 companies, 15.7%)
- **Top-heavy value:** NVIDIA ($5.48T), Alphabet ($4.81T), and Apple ($4.41T) lead a top-10 that holds a disproportionate share of total market value
- **Profitability varies structurally:** avg margin 20.7% and avg ROA 5.9% mask wide sector differences — asset-heavy sectors (banking, insurance) post low ROA by design

Full analysis in [`docs/Project_Report.pdf`](docs/Project_Report.pdf) and [`notebooks/exploratory_analysis.ipynb`](notebooks/exploratory_analysis.ipynb).

---

## 📝 Data Source & License

- **Dataset:** Forbes Global 2000 (2026), via Kaggle — subject to its own terms on the dataset page
- **Code & analysis:** MIT License (see [`LICENSE`](LICENSE))

---

## 📧 Author

**Ging (Gabriel Alegre Caña)**
Data Analyst & Dashboard Developer — Cavite State University, General Trias, PH

*Fourth project in a portfolio series: sales analytics → HR workforce → business transactions → global company analytics.*
