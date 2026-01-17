import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configure Zerve design system
plt.rcParams['figure.facecolor'] = '#1D1D20'
plt.rcParams['axes.facecolor'] = '#1D1D20'
plt.rcParams['axes.edgecolor'] = '#909094'
plt.rcParams['text.color'] = '#fbfbff'
plt.rcParams['axes.labelcolor'] = '#fbfbff'
plt.rcParams['xtick.color'] = '#fbfbff'
plt.rcParams['ytick.color'] = '#fbfbff'
plt.rcParams['grid.color'] = '#909094'
plt.rcParams['grid.alpha'] = 0.3
plt.rcParams['legend.facecolor'] = '#1D1D20'
plt.rcParams['legend.edgecolor'] = '#909094'

print("=" * 80)
print("📊 COMPREHENSIVE DATA QUALITY ANALYSIS")
print("=" * 80)

# 1. DATASET OVERVIEW
print("\n1️⃣ DATASET OVERVIEW")
print("-" * 80)
print(f"Total records: {len(integrated_dataset):,}")
print(f"Date range: {integrated_dataset['date'].min()} to {integrated_dataset['date'].max()}")
print(f"Unique states: {integrated_dataset['state'].nunique()}")
print(f"Unique districts: {integrated_dataset['district'].nunique()}")
print(f"Unique pincodes: {integrated_dataset['pincode'].nunique()}")

# 2. MISSING VALUE ANALYSIS
print("\n2️⃣ MISSING VALUE ANALYSIS")
print("-" * 80)
missing_analysis = pd.DataFrame({
    'Column': integrated_dataset.columns,
    'Missing Count': integrated_dataset.isnull().sum().values,
    'Missing %': (integrated_dataset.isnull().sum().values / len(integrated_dataset) * 100).round(2)
})
missing_analysis = missing_analysis[missing_analysis['Missing Count'] > 0].sort_values('Missing %', ascending=False)
print(missing_analysis.to_string(index=False))

total_missing_pct = (integrated_dataset.isnull().sum().sum() / (len(integrated_dataset) * len(integrated_dataset.columns)) * 100)
print(f"\nOverall missing data rate: {total_missing_pct:.2f}%")

# 3. DATA COMPLETENESS BY SOURCE
print("\n3️⃣ DATA COMPLETENESS BY SOURCE")
print("-" * 80)
enroll_complete = integrated_dataset[['age_0_5', 'age_5_17', 'age_18_greater']].notna().all(axis=1).sum()
demo_complete = integrated_dataset[['demo_age_5_17', 'demo_age_17_']].notna().all(axis=1).sum()
bio_complete = integrated_dataset[['bio_age_5_17', 'bio_age_17_']].notna().all(axis=1).sum()

print(f"Enrollment data complete: {enroll_complete:,} ({enroll_complete/len(integrated_dataset)*100:.2f}%)")
print(f"Demographic data complete: {demo_complete:,} ({demo_complete/len(integrated_dataset)*100:.2f}%)")
print(f"Biometric data complete: {bio_complete:,} ({bio_complete/len(integrated_dataset)*100:.2f}%)")

# 4. STATISTICAL SUMMARIES
print("\n4️⃣ STATISTICAL SUMMARIES - ENROLLMENT DATA")
print("-" * 80)
numeric_cols = ['age_0_5', 'age_5_17', 'age_18_greater', 'demo_age_5_17', 'demo_age_17_', 'bio_age_5_17', 'bio_age_17_']
stats = integrated_dataset[numeric_cols].describe()
print(stats.to_string())

# 5. DETECT ANOMALIES
print("\n5️⃣ ANOMALY DETECTION")
print("-" * 80)

# Check for negative values
for col in numeric_cols:
    negative_count = (integrated_dataset[col] < 0).sum()
    if negative_count > 0:
        print(f"⚠️  {col}: {negative_count:,} negative values detected")

# Check for extreme outliers (> 99.9th percentile)
print("\nExtreme outliers (values > 99.9th percentile):")
for col in numeric_cols:
    p999 = integrated_dataset[col].quantile(0.999)
    outlier_count = (integrated_dataset[col] > p999).sum()
    if outlier_count > 0:
        print(f"   {col}: {outlier_count:,} values > {p999:.0f}")

# 6. CONSISTENCY CHECKS
print("\n6️⃣ DATA CONSISTENCY CHECKS")
print("-" * 80)

# Check for duplicate geographic/temporal combinations
duplicates = integrated_dataset.duplicated(subset=['date', 'state', 'district', 'pincode'], keep=False)
print(f"Duplicate date-state-district-pincode combinations: {duplicates.sum():,}")

# Check for zero enrollments
zero_enroll = ((integrated_dataset['age_0_5'] == 0) & 
               (integrated_dataset['age_5_17'] == 0) & 
               (integrated_dataset['age_18_greater'] == 0))
print(f"Records with zero enrollment across all age groups: {zero_enroll.sum():,}")

# State name consistency
print(f"\nState name variations detected: {integrated_dataset['state'].nunique()} unique values")
state_sample = integrated_dataset['state'].value_counts().head(10)
print("\nTop 10 states by record count:")
print(state_sample.to_string())

print("\n" + "=" * 80)
print("✅ DATA QUALITY ANALYSIS COMPLETE")
print("=" * 80)