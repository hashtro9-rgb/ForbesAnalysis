from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

styles = getSampleStyleSheet()
title_style = ParagraphStyle('TitleCustom', parent=styles['Title'], fontSize=22, spaceAfter=6)
subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=11,
                                 textColor=colors.HexColor('#666666'), spaceAfter=20)
h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14, spaceBefore=18, spaceAfter=8,
                     textColor=colors.HexColor('#1a1a1a'))
body = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=15)
small = ParagraphStyle('Small', parent=styles['Normal'], fontSize=9, leading=13,
                        textColor=colors.HexColor('#555555'))

doc = SimpleDocTemplate("Data_Dictionary.pdf", pagesize=letter,
                         topMargin=0.75*inch, bottomMargin=0.75*inch,
                         leftMargin=0.75*inch, rightMargin=0.75*inch)

story = []

story.append(Paragraph("Forbes Global 2000 (2026)", title_style))
story.append(Paragraph("Data Dictionary — Cleaned Dataset Schema Reference", subtitle_style))

story.append(Paragraph("Overview", h2))
story.append(Paragraph(
    "This document describes every column in the cleaned dataset "
    "(<b>data/processed/forbes_2000_cleaned.csv</b>), including source columns retained from the raw "
    "Forbes Global 2000 export and columns engineered during the cleaning pipeline "
    "(<b>scripts/clean_forbes_2000.py</b>). The dataset contains 2,000 rows — one per ranked company — "
    "and 12 columns.", body))

# Column reference table
data = [
    ["Column", "Type", "Origin", "Description"],
    ["Rank", "int", "Source", "Forbes Global 2000 rank, 1–2000. Ties are legitimate: 298 companies share a rank with at least one other company."],
    ["Company", "str", "Source", "Company name as published by Forbes. No duplicates."],
    ["Country", "str", "Engineered", "Extracted from the raw 'Headquarters' field (split on the last comma). 62 unique countries. One row ('Klepierre') had a single-value Headquarters with no city — the value was assigned directly to Country."],
    ["City", "str", "Engineered", "Extracted from 'Headquarters' alongside Country. Null for the one row where Headquarters contained only a country name."],
    ["Industry", "str", "Source + 1 imputed", "28 industry categories. One row (Medline) was missing Industry in the raw file and was assigned 'Healthcare & Pharmaceuticals' based on the company's business profile."],
    ["Sales ($B)", "float", "Source", "Annual revenue in billions of US dollars. No missing or negative values."],
    ["Profit ($B)", "float", "Source", "Net profit in billions of US dollars. No missing or negative values."],
    ["Assets ($B)", "float", "Source", "Total assets in billions of US dollars. No missing or negative values."],
    ["Market Value ($B)", "float", "Source", "Market capitalization in billions of US dollars. One row (Revolution Medicines) is missing this value and was left as null rather than imputed."],
    ["Profit_Margin_%", "float", "Derived", "(Profit ($B) / Sales ($B)) × 100. Rounded to 2 decimals."],
    ["Asset_Efficiency", "float", "Derived", "Sales ($B) / Assets ($B). Rounded to 3 decimals. Higher values indicate more revenue generated per dollar of assets."],
    ["ROA_%", "float", "Derived", "(Profit ($B) / Assets ($B)) × 100 — Return on Assets. Rounded to 2 decimals."],
]

col_widths = [1.15*inch, 0.55*inch, 0.85*inch, 3.35*inch]
table = Table(data, colWidths=col_widths, repeatRows=1)
table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a1a1a')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 9),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,1), (-1,-1), 8),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f5f5f5')]),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(table)

story.append(Paragraph("Known Data Quality Notes", h2))
notes = [
    "<b>Duplicate ranks are expected, not an error.</b> Forbes ties companies at the same rank when their composite scores match; 298 of 2,000 rows share a rank with another company.",
    "<b>Outlier profit margins are retained.</b> A small number of companies (e.g. Broadcom, at roughly 2,484%) show profit margins far above 100% due to one-off accounting events (such as large asset sales or tax adjustments) relative to a small revenue base. These are flagged in the quality report but not removed or capped, since they reflect the source data accurately.",
    "<b>Two rows retain nulls after cleaning by design:</b> Market Value ($B) for Revolution Medicines (no reliable way to estimate it from other columns), and City for Klepierre (Headquarters listed only a country).",
]
for n in notes:
    story.append(Paragraph("• " + n, body))
    story.append(Spacer(1, 6))

story.append(Paragraph("Related Files", h2))
story.append(Paragraph(
    "<b>data/raw/Forbes_2000_Companies_2026.csv</b> — original unmodified export (8 columns).<br/>"
    "<b>data/processed/forbes_2000_cleaned.csv</b> — this schema (12 columns).<br/>"
    "<b>data/reports/data_quality_report.txt</b> — full completeness metrics and cleaning log.<br/>"
    "<b>scripts/clean_forbes_2000.py</b> — the cleaning pipeline that produces this dataset from raw.<br/>"
    "<b>tests/test_data_quality.py</b> — automated tests that validate this schema and its constraints.",
    small))

doc.build(story)
print("Data_Dictionary.pdf created")
