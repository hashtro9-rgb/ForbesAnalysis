from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, ListFlowable, ListItem)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

styles = getSampleStyleSheet()
title_style = ParagraphStyle('TitleCustom', parent=styles['Title'], fontSize=22, spaceAfter=4)
subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=11,
                                 textColor=colors.HexColor('#666666'), spaceAfter=22)
h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=15, spaceBefore=18, spaceAfter=8,
                     textColor=colors.HexColor('#1a1a1a'))
h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=11.5, spaceBefore=10, spaceAfter=4,
                     textColor=colors.HexColor('#333333'))
body = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=15, spaceAfter=6)
bullet = ParagraphStyle('Bullet', parent=body, leftIndent=14, spaceAfter=4)
note = ParagraphStyle('Note', parent=body, textColor=colors.HexColor('#8a6d00'),
                       backColor=colors.HexColor('#fff8e1'), borderPadding=8, leading=14)

doc = SimpleDocTemplate("Dashboard_Guide.pdf", pagesize=letter,
                         topMargin=0.75*inch, bottomMargin=0.75*inch,
                         leftMargin=0.75*inch, rightMargin=0.75*inch)

story = []

story.append(Paragraph("Forbes Global 2000 Dashboard", title_style))
story.append(Paragraph("User Guide — How to Read and Navigate the Dashboard", subtitle_style))

story.append(Paragraph("Getting Started", h1))
story.append(Paragraph(
    "The dashboard is a single self-contained HTML file (<b>dashboard/index.html</b>, with "
    "<b>style.css</b> and <b>script.js</b> alongside it). Open <b>index.html</b> directly in any modern "
    "browser — no installation, server, or internet connection required after the page loads (only the "
    "Google Fonts and Chart.js CDN references need connectivity; the company data itself is embedded in "
    "the page).", body))

story.append(Paragraph("Layout Overview", h1))

layout_data = [
    ["Area", "What it does"],
    ["Sidebar (left)", "Jump to any section of the dashboard: Overview, Market Leaders, Country Insights, "
     "Industry Analysis, Profitability, Insights, or Company Explorer."],
    ["KPI Row (top)", "Five headline numbers: total companies, combined sales, combined profit, average "
     "profit margin, and countries × industries represented — all recalculated live as filters change."],
    ["Filters Panel (right)", "Country, Industry, Rank Range, and Profitability tier dropdowns, plus a "
     "company name search box. Every filter affects the entire dashboard at once."],
    ["Chart Grid (center)", "Five linked visualizations covering market value by rank tier, industry mix, "
     "top industries, margin distribution, and average ROA by rank tier."],
    ["Country Heat-Grid", "A shaded grid of countries by company count — a compact substitute for a "
     "geographic map."],
    ["Top 10 Leaderboard", "The highest market-value companies within whatever subset is currently filtered."],
    ["Insights & Recommendations", "Auto-generated takeaways — market concentration, geographic exposure, "
     "and margin split — plus three plain-language recommendations, recalculated on every filter change."],
    ["Company Explorer", "A full sortable, searchable table of the filtered companies. Click any column "
     "header to sort by that field."],
]
layout_table = Table(layout_data, colWidths=[1.6*inch, 3.9*inch])
layout_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a1a1a')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f5f5f5')]),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(layout_table)

story.append(Paragraph("Using the Filters", h1))
story.append(Paragraph(
    "All five filters combine with AND logic — for example, selecting Country = \"Japan\" and "
    "Industry = \"Banking\" shows only Japanese banks, not all Japanese companies or all banks.", body))

filter_points = [
    "<b>Country / Industry:</b> dropdown lists always show every value present in the full 2,000-company "
    "dataset, regardless of current filters — so you can always pivot to a different country or industry "
    "without resetting first.",
    "<b>Rank Range:</b> Top 100, 101–500, 501–1000, or 1001–2000 — useful for comparing mega-caps against "
    "the long tail of the list.",
    "<b>Profitability tier:</b> High (margin above 20%), Mid (5–20%), or Low (below 5%).",
    "<b>Search:</b> matches company name as you type, case-insensitive, combined with any other active filters.",
    "<b>Reset all filters</b> (bottom of the filters panel) clears every filter and search term in one click.",
]
story.append(ListFlowable([ListItem(Paragraph(s, bullet), leftIndent=10) for s in filter_points],
                          bulletType='bullet', start='•'))

story.append(Paragraph(
    "Every part of the dashboard — KPIs, charts, the heat-grid, the leaderboard, the insights cards, and "
    "the table — updates together whenever a filter changes. If a filter combination matches zero "
    "companies, panels will show a \"No matches\" state instead of stale data.", note))

story.append(Paragraph("Reading the Insights Panel", h1))
story.append(Paragraph(
    "The Insights & Recommendations section is not static commentary — it recalculates from whichever "
    "companies are currently visible. Three observational cards describe the current view (market value "
    "concentration in the top 10, the leading country's share, and the margin split), followed by three "
    "recommendation cards that respond to those numbers — for example, flagging diversification risk if "
    "the top 10 companies hold more than 40% of combined market value in the current filter.", body))

story.append(Paragraph("Sorting the Company Table", h1))
story.append(Paragraph(
    "Click any column header in the Company Explorer to sort by that column; click the same header again "
    "to reverse the sort direction. The active sort column and direction are shown in the table's footer. "
    "The table displays up to 60 rows at a time — narrow your filters or search to bring a specific company "
    "into view.", body))

story.append(Paragraph("Color Coding", h1))
story.append(Paragraph(
    "The dashboard uses a single \"Trading Floor\" visual theme: a near-black background with a gold "
    "accent color for primary data (bars, the leaderboard, headline numbers), and green / red coding "
    "specifically on Profit Margin % and ROA % figures — green for positive, red for negative — similar "
    "to a live market ticker.", body))

story.append(Paragraph("Troubleshooting", h1))
trouble = [
    "<b>Charts don't appear:</b> confirm an internet connection is available on first load — the dashboard "
    "loads Chart.js and Google Fonts from a CDN. The company data itself does not require a connection, "
    "since it is embedded in the page.",
    "<b>Opened the file but nothing loads:</b> make sure you're opening <b>index.html</b>, not "
    "<b>style.css</b> or <b>script.js</b> directly — those are supporting files, not the entry point.",
    "<b>Filters seem \"stuck\":</b> use the <b>Reset all filters</b> button at the bottom of the filters "
    "panel rather than manually clearing each dropdown.",
]
story.append(ListFlowable([ListItem(Paragraph(s, bullet), leftIndent=10) for s in trouble],
                          bulletType='bullet', start='•'))

doc.build(story)
print("Dashboard_Guide.pdf created")
