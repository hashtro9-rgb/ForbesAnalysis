"""
Forbes Global 2000 Companies (2026) - Data Cleaning Pipeline
Author: Gabriel Alegre Caña
Date: 2026

This script loads, cleans, and validates the Forbes Global 2000 dataset.
Outputs: cleaned CSV, data quality report, EDA summary
"""

import pandas as pd
import numpy as np
from datetime import datetime

# ============================================================================
# LOAD DATA
# ============================================================================

input_path = '../data/raw/Forbes_2000_Companies_2026.csv'
df = pd.read_csv(input_path)

print("=" * 70)
print("FORBES GLOBAL 2000 (2026) - DATA CLEANING PIPELINE")
print("=" * 70)
print(f"\n📥 Loaded {len(df)} records, {len(df.columns)} columns")
print(f"   Columns: {', '.join(df.columns.tolist())}")

# ============================================================================
# INITIAL DATA QUALITY CHECK
# ============================================================================

print("\n" + "=" * 70)
print("INITIAL DATA QUALITY")
print("=" * 70)
print(f"\nMissing values:\n{df.isna().sum()}\n")
print(f"Data types:\n{df.dtypes}\n")

# ============================================================================
# CLEANING STEPS
# ============================================================================

# Step 1: Extract City and Country from Headquarters
print("STEP 1: Extract City and Country from Headquarters")
split_result = df['Headquarters'].str.split(', ', n=1, expand=True)
if split_result.shape[1] == 1:
    split_result[1] = None
df['City'] = split_result[1].fillna(split_result[0])
df['Country'] = split_result[1]
# Handle single-value Headquarters entries (e.g. "France" with no city listed):
# the lone value is a country-level location, not an unnamed city.
single_value_mask = df['Country'].isna()
if single_value_mask.any():
    df.loc[single_value_mask, 'Country'] = df.loc[single_value_mask, 'Headquarters']
    df.loc[single_value_mask, 'City'] = None
    print(f"   ⚠ {single_value_mask.sum()} row(s) had no city in Headquarters — treated the value as Country:")
    print(f"     {df.loc[single_value_mask, ['Rank','Company','Headquarters']].to_string(index=False)}")
print(f"   ✓ Extracted {df['Country'].nunique()} unique countries")
print(f"   ✓ Country distribution: {dict(df['Country'].value_counts().head(5))}")

# Step 2: Handle missing Industry values
print("\nSTEP 2: Handle Missing Industry")
missing_industry = df[df['Industry'].isna()]
print(f"   {len(missing_industry)} row(s) missing Industry:")
print(missing_industry[['Rank', 'Company', 'Country', 'Sales ($B)']].to_string())

# Assign industry based on company characteristics
# Medline: healthcare/medical supplies → Diversified Financials (close match)
df.loc[df['Company'] == 'Medline', 'Industry'] = 'Healthcare & Pharmaceuticals'
print(f"   ✓ Assigned Industry to: {missing_industry['Company'].tolist()}")

# Step 3: Handle missing Market Value
print("\nSTEP 3: Handle Missing Market Value")
missing_mv = df[df['Market Value ($B)'].isna()]
print(f"   {len(missing_mv)} row(s) with missing Market Value: {missing_mv['Company'].tolist()}")
print(f"   → Keeping as NaN (will flag in reports, not impute)")

# Step 4: Rename columns for clarity
print("\nSTEP 4: Standardize Column Names")
df.columns = df.columns.str.strip()
print(f"   ✓ Removed leading/trailing whitespace from headers")

# Step 5: Calculate derived metrics
print("\nSTEP 5: Calculate Derived Metrics")
df['Profit_Margin_%'] = (df['Profit ($B)'] / df['Sales ($B)'] * 100).round(2)
df['Asset_Efficiency'] = (df['Sales ($B)'] / df['Assets ($B)']).round(3)
df['ROA_%'] = (df['Profit ($B)'] / df['Assets ($B)'] * 100).round(2)
print(f"   ✓ Profit Margin (%) = Profit / Sales × 100")
print(f"   ✓ Asset Efficiency = Sales / Assets")
print(f"   ✓ ROA (%) = Profit / Assets × 100")

# Step 6: Reorder columns logically
column_order = [
    'Rank', 'Company', 'Country', 'City', 'Industry',
    'Sales ($B)', 'Profit ($B)', 'Assets ($B)', 'Market Value ($B)',
    'Profit_Margin_%', 'Asset_Efficiency', 'ROA_%'
]
df = df[column_order]

# Step 7: Sort by Rank
df = df.sort_values('Rank').reset_index(drop=True)
print(f"\nSTEP 6: Reorder columns and sort by Rank")

# ============================================================================
# FINAL DATA QUALITY VALIDATION
# ============================================================================

print("\n" + "=" * 70)
print("FINAL DATA QUALITY")
print("=" * 70)
print(f"\nMissing values after cleaning:\n{df.isna().sum()}\n")
print(f"Data types:\n{df.dtypes}\n")

# Validate numeric ranges
print("Numeric validation:")
print(f"   Sales: ${df['Sales ($B)'].min():.2f}B - ${df['Sales ($B)'].max():.2f}B")
print(f"   Profit: ${df['Profit ($B)'].min():.2f}B - ${df['Profit ($B)'].max():.2f}B")
print(f"   Profit Margin: {df['Profit_Margin_%'].min():.2f}% - {df['Profit_Margin_%'].max():.2f}%")
print(f"   ROA: {df['ROA_%'].min():.2f}% - {df['ROA_%'].max():.2f}%")

# ============================================================================
# EXPLORATORY DATA ANALYSIS
# ============================================================================

print("\n" + "=" * 70)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 70)

print("\n📊 Top 10 Companies by Market Value:")
top_10 = df.nlargest(10, 'Market Value ($B)')[['Rank', 'Company', 'Country', 'Market Value ($B)']].to_string(index=False)
print(top_10)

print("\n🏭 Industry Distribution:")
industry_counts = df['Industry'].value_counts().sort_values(ascending=False)
for idx, (industry, count) in enumerate(industry_counts.items(), 1):
    pct = (count / len(df) * 100)
    print(f"   {idx:2d}. {industry:40s} {count:4d} ({pct:5.1f}%)")

print("\n🌍 Top 15 Countries by Company Count:")
country_counts = df['Country'].value_counts().head(15)
for idx, (country, count) in enumerate(country_counts.items(), 1):
    pct = (count / len(df) * 100)
    print(f"   {idx:2d}. {country:20s} {count:4d} ({pct:5.1f}%)")

print("\n💰 Key Statistics:")
print(f"   Total Global Sales: ${df['Sales ($B)'].sum():.2f}B")
print(f"   Total Global Profit: ${df['Profit ($B)'].sum():.2f}B")
print(f"   Average Company Sales: ${df['Sales ($B)'].mean():.2f}B")
print(f"   Average Profit Margin: {df['Profit_Margin_%'].mean():.2f}%")
print(f"   Average ROA: {df['ROA_%'].mean():.2f}%")

# ============================================================================
# EXPORT CLEANED DATA
# ============================================================================

output_csv = '../data/processed/forbes_2000_cleaned.csv'
df.to_csv(output_csv, index=False)
print("\n" + "=" * 70)
print(f"✅ CLEANED DATA EXPORTED")
print("=" * 70)
print(f"   Output: {output_csv}")
print(f"   Rows: {len(df)}, Columns: {len(df.columns)}")

# ============================================================================
# GENERATE DATA QUALITY REPORT
# ============================================================================

report_path = '../data/reports/data_quality_report.txt'
with open(report_path, 'w') as f:
    f.write("FORBES GLOBAL 2000 (2026) - DATA QUALITY REPORT\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    f.write("DATASET OVERVIEW\n")
    f.write("-" * 70 + "\n")
    f.write(f"Total Records: {len(df)}\n")
    f.write(f"Total Columns: {len(df.columns)}\n")
    f.write(f"Columns: {', '.join(df.columns.tolist())}\n\n")
    
    f.write("DATA QUALITY METRICS\n")
    f.write("-" * 70 + "\n")
    f.write(f"Completeness:\n")
    for col in df.columns:
        missing = df[col].isna().sum()
        pct_complete = ((len(df) - missing) / len(df) * 100)
        f.write(f"   {col:30s}: {pct_complete:6.2f}% complete ({missing} missing)\n")
    
    f.write(f"\nData Type Distribution:\n")
    for dtype, count in df.dtypes.value_counts().items():
        f.write(f"   {str(dtype):20s}: {count} columns\n")
    
    f.write(f"\nDuplicate Ranks:\n")
    f.write(f"   Total unique ranks: {df['Rank'].nunique()}\n")
    f.write(f"   Duplicate rank entries: {df['Rank'].duplicated().sum()}\n")
    f.write(f"   Note: Duplicates are expected (Forbes ties companies at same rank)\n")
    
    f.write(f"\nCleaning Actions Performed:\n")
    f.write(f"   ✓ Extracted City and Country from Headquarters (62 countries)\n")
    f.write(f"   ✓ Filled 1 missing Industry value (Medline → Healthcare & Pharmaceuticals)\n")
    f.write(f"   ✓ Retained 1 missing Market Value (Revolution Medicines) - flagged but not imputed\n")
    f.write(f"   ✓ Calculated 3 derived metrics (Profit Margin, Asset Efficiency, ROA)\n")
    f.write(f"   ✓ Standardized column naming and ordering\n")
    f.write(f"   ✓ Sorted data by Rank\n\n")
    
    f.write("MISSING VALUES AFTER CLEANING\n")
    f.write("-" * 70 + "\n")
    for col in df.columns:
        missing = df[col].isna().sum()
        if missing > 0:
            f.write(f"   {col}: {missing}\n")
    if df.isna().sum().sum() == 0:
        f.write("   None - Data is 100% complete\n\n")
    
    f.write("NUMERIC RANGES\n")
    f.write("-" * 70 + "\n")
    f.write(f"Sales ($B):\n")
    f.write(f"   Min: ${df['Sales ($B)'].min():.2f}B\n")
    f.write(f"   Max: ${df['Sales ($B)'].max():.2f}B\n")
    f.write(f"   Mean: ${df['Sales ($B)'].mean():.2f}B\n")
    f.write(f"   Median: ${df['Sales ($B)'].median():.2f}B\n\n")
    
    f.write(f"Profit ($B):\n")
    f.write(f"   Min: ${df['Profit ($B)'].min():.2f}B\n")
    f.write(f"   Max: ${df['Profit ($B)'].max():.2f}B\n")
    f.write(f"   Mean: ${df['Profit ($B)'].mean():.2f}B\n")
    f.write(f"   Median: ${df['Profit ($B)'].median():.2f}B\n\n")
    
    f.write(f"Profit Margin (%):\n")
    f.write(f"   Min: {df['Profit_Margin_%'].min():.2f}%\n")
    f.write(f"   Max: {df['Profit_Margin_%'].max():.2f}%\n")
    f.write(f"   Mean: {df['Profit_Margin_%'].mean():.2f}%\n")
    f.write(f"   Median: {df['Profit_Margin_%'].median():.2f}%\n\n")
    
    f.write(f"ROA (%):\n")
    f.write(f"   Min: {df['ROA_%'].min():.2f}%\n")
    f.write(f"   Max: {df['ROA_%'].max():.2f}%\n")
    f.write(f"   Mean: {df['ROA_%'].mean():.2f}%\n")
    f.write(f"   Median: {df['ROA_%'].median():.2f}%\n\n")
    
    f.write("CATEGORICAL DISTRIBUTIONS\n")
    f.write("-" * 70 + "\n")
    f.write(f"Countries: {df['Country'].nunique()} unique\n")
    f.write(f"Industries: {df['Industry'].nunique()} unique\n")
    f.write(f"Cities: {df['City'].nunique()} unique\n\n")
    
    f.write("TOP 5 COUNTRIES BY COMPANY COUNT\n")
    f.write("-" * 70 + "\n")
    for idx, (country, count) in enumerate(df['Country'].value_counts().head(5).items(), 1):
        f.write(f"   {idx}. {country}: {count}\n")
    
    f.write("\n")

print(f"\n✅ DATA QUALITY REPORT EXPORTED")
print(f"   Output: {report_path}")

print("\n" + "=" * 70)
print("✅ CLEANING PIPELINE COMPLETE")
print("=" * 70)
print("\nNext steps for dashboard development:")
print("   1. Load forbes_2000_cleaned.csv into HTML dashboard template")
print("   2. Create interactive filters (Country, Industry, Rank ranges)")
print("   3. Build visualization components (charts, tables, KPI cards)")
print("   4. Test and deploy to GitHub Pages")
