from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, ListFlowable, ListItem)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

styles = getSampleStyleSheet()
title_style = ParagraphStyle('TitleCustom', parent=styles['Title'], fontSize=24, spaceAfter=4)
subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=11,
                                 textColor=colors.HexColor('#666666'), spaceAfter=4)
meta_style = ParagraphStyle('Meta', parent=styles['Normal'], fontSize=9,
                             textColor=colors.HexColor('#999999'), spaceAfter=22)
h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=16, spaceBefore=20, spaceAfter=8,
                     textColor=colors.HexColor('#1a1a1a'))
h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=12.5, spaceBefore=14, spaceAfter=6,
                     textColor=colors.HexColor('#333333'))
body = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=15, spaceAfter=8)
bullet = ParagraphStyle('Bullet', parent=body, leftIndent=14, spaceAfter=4)
stat_label = ParagraphStyle('StatLabel', parent=styles['Normal'], fontSize=8.5,
                              textColor=colors.HexColor('#777777'))
stat_value = ParagraphStyle('StatValue', parent=styles['Normal'], fontSize=16,
                              textColor=colors.HexColor('#B8860B'), fontName='Helvetica-Bold')

doc = SimpleDocTemplate("Project_Report.pdf", pagesize=letter,
                         topMargin=0.75*inch, bottomMargin=0.75*inch,
                         leftMargin=0.75*inch, rightMargin=0.75*inch)

story = []

story.append(Paragraph("Forbes Global 2000 (2026)", title_style))
story.append(Paragraph("Analytics Dashboard — Project Report", subtitle_style))
story.append(Paragraph("Author: Ging (Gabriel Alegre Caña) &nbsp;&nbsp;|&nbsp;&nbsp; Cavite State University &nbsp;&nbsp;|&nbsp;&nbsp; July 2026", meta_style))

# --- Key stats row ---
stats = [
    ("2,000", "Companies Analyzed"),
    ("62", "Countries"),
    ("$55.96T", "Combined Sales"),
    ("$5.98T", "Combined Profit"),
]
stat_table_data = [[Paragraph(v, stat_value) for v,l in stats], [Paragraph(l, stat_label) for v,l in stats]]
stat_table = Table(stat_table_data, colWidths=[1.55*inch]*4)
stat_table.setStyle(TableStyle([
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('BOTTOMPADDING', (0,0), (-1,0), 2),
    ('TOPPADDING', (0,0), (-1,-1), 0),
    ('LINEBELOW', (0,-1), (-1,-1), 0.75, colors.HexColor('#dddddd')),
    ('BOTTOMPADDING', (0,-1), (-1,-1), 14),
]))
story.append(stat_table)

story.append(Paragraph("1. Project Overview", h1))
story.append(Paragraph(
    "This project takes the Forbes Global 2000 (2026) dataset — the world's 2,000 largest public companies, "
    "ranked by a composite of sales, profit, assets, and market value — and turns it into a complete portfolio "
    "artifact: a documented data cleaning pipeline, automated data quality tests, an exploratory analysis "
    "notebook, and a self-contained interactive BI-style dashboard.", body))
story.append(Paragraph(
    "The goal was not just to visualize the dataset, but to demonstrate a full, defensible analytics workflow "
    "end to end — the kind of process a client or employer could inspect at any stage and trust.", body))

story.append(Paragraph("2. Data Cleaning Pipeline", h1))
story.append(Paragraph(
    "The raw export (<b>data/raw/Forbes_2000_Companies_2026.csv</b>) contained 2,000 rows and 8 columns. "
    "The cleaning script (<b>scripts/clean_forbes_2000.py</b>) performed the following steps:", body))

steps = [
    "<b>Split 'Headquarters' into City and Country.</b> One row ('Klepierre') listed only a country with no "
    "city — this was caught by an automated test and the split logic was corrected to treat single-value "
    "Headquarters entries as Country rather than silently misfiling them as City.",
    "<b>Filled 1 missing Industry value</b> (Medline) based on its business profile, since the field cannot "
    "be reliably inferred from other columns without domain judgment.",
    "<b>Left 1 missing Market Value as null</b> (Revolution Medicines) rather than imputing it — there is no "
    "reliable way to estimate market capitalization from the other financial columns, and a fabricated value "
    "would be worse than an honest gap.",
    "<b>Engineered three derived financial metrics</b> from source columns only: Profit Margin %, "
    "Asset Efficiency, and Return on Assets (ROA %).",
    "<b>Validated the output</b> against 12 automated tests covering row counts, schema, duplicate detection, "
    "value ranges, and a spot-check that recalculates Profit Margin from source columns to confirm the "
    "derived metric is computed correctly.",
]
story.append(ListFlowable([ListItem(Paragraph(s, bullet), leftIndent=10) for s in steps],
                          bulletType='bullet', start='•'))

story.append(Paragraph("3. Data Quality Summary", h1))
dq_data = [
    ["Metric", "Result"],
    ["Total rows", "2,000"],
    ["Total columns (after cleaning)", "12"],
    ["Overall completeness", "99.95%"],
    ["Unique countries", "62"],
    ["Unique industries", "28"],
    ["Duplicate company names", "0"],
    ["Duplicate ranks (expected ties)", "298"],
    ["Automated tests passing", "12 / 12"],
]
dq_table = Table(dq_data, colWidths=[3.2*inch, 2.2*inch])
dq_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a1a1a')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9.5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f5f5f5')]),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(dq_table)

story.append(Paragraph("4. Key Findings", h1))
story.append(Paragraph("Geographic distribution", h2))
story.append(Paragraph(
    "The United States accounts for 595 of the 2,000 companies (29.8%), followed by China (300), Japan (178), "
    "South Korea (66), and Canada (64). Together the top 5 countries account for over 60% of all listed companies.", body))

story.append(Paragraph("Industry concentration", h2))
story.append(Paragraph(
    "Banking is the single largest industry by company count (314 companies, 15.7%), reflecting how "
    "capital-intensive, regionally-fragmented banking sectors produce many nationally significant but "
    "individually smaller institutions. Diversified Financials, Construction, Insurance, and Capital Goods "
    "round out the top five.", body))

story.append(Paragraph("Market value concentration", h2))
story.append(Paragraph(
    "The 10 largest companies by market value — led by NVIDIA ($5.48T), Alphabet ($4.81T), and Apple ($4.41T) "
    "— represent a disproportionate share of total market value across the full 2,000-company list, "
    "illustrating how concentrated the upper tail of global market capitalization has become.", body))

story.append(Paragraph("Profitability spread", h2))
story.append(Paragraph(
    "Average profit margin across all companies is 20.72%, and average ROA is 5.89% — but both figures mask "
    "wide variation. A handful of companies post extreme outlier margins (e.g. Broadcom, ~2,484%) tied to "
    "one-off financial events rather than typical operating profitability, while many asset-heavy sectors "
    "(banking, insurance) post structurally lower ROA by nature of their business model.", body))

story.append(PageBreak())

story.append(Paragraph("5. Dashboard Design", h1))
story.append(Paragraph(
    "The dashboard (<b>dashboard/index.html</b>) follows a BI-tool layout rather than an editorial/report "
    "layout: sidebar navigation, a KPI row, a persistent filters panel, a grid of linked charts, and a "
    "sortable company table.", body))
story.append(Paragraph("Key design decisions:", h2))
design_points = [
    "<b>Single visual language.</b> A \"Trading Floor\" palette — near-black background, gold accent, "
    "green/red gain-loss coding on margin and ROA figures — was chosen deliberately over a multi-theme "
    "switcher, to keep the ticker-style profitability coding meaningful and consistent.",
    "<b>Data embedded inline.</b> Rather than fetching the CSV at runtime, the cleaned dataset is embedded "
    "directly as JSON inside the dashboard's JavaScript. This removes a CORS/file-protocol failure mode "
    "when the dashboard is opened directly (rather than served), and means the dashboard deploys as a "
    "single self-contained unit.",
    "<b>Unified filter state.</b> Every filter (Country, Industry, Rank Range, Profitability tier, and "
    "search) runs through a single update function that recomputes the KPIs, every chart, the country "
    "breakdown, the leaderboard, the computed insights, and the table together — so no part of the "
    "dashboard can show a view inconsistent with the current filters.",
    "<b>Computed, not hardcoded, insights.</b> The Insights & Recommendations panel recalculates its "
    "narrative (market concentration, geographic exposure, margin split, and industry leaders) from "
    "whichever subset of companies is currently filtered, rather than displaying static text.",
]
story.append(ListFlowable([ListItem(Paragraph(s, bullet), leftIndent=10) for s in design_points],
                          bulletType='bullet', start='•'))

story.append(Paragraph("6. Testing & Validation", h1))
story.append(Paragraph(
    "A pytest suite (<b>tests/test_data_quality.py</b>) validates the cleaned dataset on every run: row "
    "counts, expected columns, duplicate detection, value ranges, missing-value bounds, and a numerical "
    "spot-check that recomputes Profit Margin % from source columns to confirm the derived metric matches "
    "within rounding tolerance. This test suite caught a real bug during development — a single-value "
    "Headquarters entry that was silently misclassified during the City/Country split — which was then "
    "fixed at the source in the cleaning script rather than patched downstream.", body))

story.append(Paragraph("7. Deployment", h1))
story.append(Paragraph(
    "The dashboard is deployed via GitHub Pages, automated through a GitHub Actions workflow "
    "(<b>.github/workflows/deploy.yml</b>) that publishes the contents of the <b>dashboard/</b> directory "
    "on every push to the main branch. Because the dataset is embedded rather than fetched separately, "
    "the deployed dashboard has no external data dependency.", body))

story.append(Paragraph("8. Skills Demonstrated", h1))
skills = [
    "End-to-end data pipeline design: raw data → validated, cleaned, tested output",
    "Root-cause debugging (fixing a data-splitting edge case at the source, not patching symptoms)",
    "Automated testing discipline for data quality, not just application code",
    "Front-end dashboard engineering: state management, dynamic chart re-rendering, computed insights",
    "Technical documentation: data dictionary, architecture notes, and this report",
    "Deployment automation via CI/CD (GitHub Actions → GitHub Pages)",
]
story.append(ListFlowable([ListItem(Paragraph(s, bullet), leftIndent=10) for s in skills],
                          bulletType='bullet', start='•'))

story.append(Spacer(1, 20))
story.append(Paragraph(
    "Data source: Forbes Global 2000 (2026), via Kaggle. See README.md for full attribution and license notes.",
    stat_label))

doc.build(story)
print("Project_Report.pdf created")
