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

zerve_colors = ['#A1C9F4', '#FFB482', '#8DE5A1', '#FF9F9B', '#D0BBFF', 
                '#1F77B4', '#9467BD', '#8C564B', '#C49C94', '#E377C2']

print("=" * 80)
print("🔐 BIOMETRIC MODALITY USAGE ANALYSIS")
print("=" * 80)

# Filter to biometric data only
bio_df = integrated_dataset[integrated_dataset[['bio_age_5_17', 'bio_age_17_']].notna().all(axis=1)].copy()

print("\n📊 BIOMETRIC DATA OVERVIEW")
print("-" * 80)
print(f"Total biometric records: {len(bio_df):,}")
print(f"Date range: {bio_df['date'].min()} to {bio_df['date'].max()}")
print(f"States covered: {bio_df['state'].nunique()}")
print(f"Districts covered: {bio_df['district'].nunique()}")

# Age group analysis for biometric
total_bio_5_17 = bio_df['bio_age_5_17'].sum()
total_bio_17_plus = bio_df['bio_age_17_'].sum()
total_bio_enrollments = total_bio_5_17 + total_bio_17_plus

print("\n\n📈 BIOMETRIC AGE GROUP DISTRIBUTION")
print("-" * 80)
print(f"\nAge 5-17:")
print(f"  Total: {total_bio_5_17:,.0f}")
print(f"  Percentage: {total_bio_5_17/total_bio_enrollments*100:.2f}%")
print(f"  Average per record: {bio_df['bio_age_5_17'].mean():.2f}")
print(f"  Median: {bio_df['bio_age_5_17'].median():.2f}")
print(f"  Std Dev: {bio_df['bio_age_5_17'].std():.2f}")

print(f"\nAge 17+:")
print(f"  Total: {total_bio_17_plus:,.0f}")
print(f"  Percentage: {total_bio_17_plus/total_bio_enrollments*100:.2f}%")
print(f"  Average per record: {bio_df['bio_age_17_'].mean():.2f}")
print(f"  Median: {bio_df['bio_age_17_'].median():.2f}")
print(f"  Std Dev: {bio_df['bio_age_17_'].std():.2f}")

print(f"\nTotal biometric enrollments: {total_bio_enrollments:,.0f}")

# Regional analysis
print("\n\n🗺️  BIOMETRIC USAGE BY STATE (Top 15)")
print("-" * 80)

state_bio = bio_df.groupby('state').agg({
    'bio_age_5_17': 'sum',
    'bio_age_17_': 'sum',
    'pincode': 'count'
}).rename(columns={'pincode': 'record_count'})

state_bio['total_biometric'] = state_bio['bio_age_5_17'] + state_bio['bio_age_17_']
state_bio['avg_per_record'] = state_bio['total_biometric'] / state_bio['record_count']
state_bio['pct_5_17'] = (state_bio['bio_age_5_17'] / state_bio['total_biometric'] * 100).round(2)
state_bio['pct_17_plus'] = (state_bio['bio_age_17_'] / state_bio['total_biometric'] * 100).round(2)
state_bio = state_bio.sort_values('total_biometric', ascending=False)

print("\nTop 15 States by Total Biometric Enrollments:")
print(state_bio.head(15)[['total_biometric', 'record_count', 'avg_per_record', 'pct_5_17', 'pct_17_plus']].to_string())

# Biometric type analysis
print("\n\n🔍 BIOMETRIC MODALITY TYPE ANALYSIS")
print("-" * 80)
print("NOTE: The current dataset provides age-grouped biometric counts but does not")
print("include specific modality types (fingerprint, iris, facial recognition).")
print("\nBased on Aadhaar system specifications:")
print("  • Fingerprints: Primary biometric for adults (10 fingerprints)")
print("  • Iris scans: Secondary biometric for adults (both eyes)")
print("  • Facial photo: Required for all age groups")
print("  • Age 5-17: Typically uses fingerprints + photo (iris optional)")
print("  • Age 17+: All three modalities (fingerprints, iris, photo)")
print("\nTo analyze actual modality usage frequencies, granular biometric type data")
print("would be required from the Aadhaar enrollment system.")

# Biometric coverage analysis
print("\n\n📊 BIOMETRIC COVERAGE ANALYSIS")
print("-" * 80)

# Compare biometric vs enrollment data where both exist
merged_complete = integrated_dataset[
    integrated_dataset[['age_0_5', 'age_5_17', 'age_18_greater', 'bio_age_5_17', 'bio_age_17_']].notna().all(axis=1)
].copy()

print(f"\nRecords with both enrollment and biometric data: {len(merged_complete):,}")

if len(merged_complete) > 0:
    # Calculate biometric capture rates
    merged_complete['enroll_5_17'] = merged_complete['age_5_17']
    merged_complete['enroll_17_plus'] = merged_complete['age_18_greater']
    
    bio_capture_5_17 = merged_complete['bio_age_5_17'].sum() / merged_complete['enroll_5_17'].sum() * 100
    bio_capture_17_plus = merged_complete['bio_age_17_'].sum() / merged_complete['enroll_17_plus'].sum() * 100
    
    print(f"\nBiometric capture rates (in overlapping records):")
    print(f"  Age 5-17: {bio_capture_5_17:.2f}%")
    print(f"  Age 17+: {bio_capture_17_plus:.2f}%")

# Create visualizations
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Chart 1: Top 12 States by Biometric Enrollments
top_12_bio = state_bio.head(12)
bars = ax1.barh(range(len(top_12_bio)), top_12_bio['total_biometric']/1000000, color=zerve_colors[3])
ax1.set_yticks(range(len(top_12_bio)))
ax1.set_yticklabels(top_12_bio.index, fontsize=10)
ax1.set_xlabel('Total Biometric Enrollments (millions)', fontsize=12, color='#fbfbff')
ax1.set_title('Top 12 States by Biometric Enrollments', fontsize=14, fontweight='bold', color='#fbfbff', pad=20)
ax1.invert_yaxis()

for i, (idx, row) in enumerate(top_12_bio.iterrows()):
    ax1.text(row['total_biometric']/1000000 + 0.1, i, f"{row['total_biometric']/1000000:.2f}M", 
             va='center', fontsize=9, color='#fbfbff')

# Chart 2: Age Group Distribution in Biometric Data
age_group_labels = ['Age 5-17', 'Age 17+']
age_group_values = [total_bio_5_17, total_bio_17_plus]
age_group_pcts = [total_bio_5_17/total_bio_enrollments*100, total_bio_17_plus/total_bio_enrollments*100]

bars = ax2.bar(range(len(age_group_labels)), age_group_pcts, color=[zerve_colors[0], zerve_colors[1]])
ax2.set_xticks(range(len(age_group_labels)))
ax2.set_xticklabels(age_group_labels, fontsize=11)
ax2.set_ylabel('Percentage of Total Biometric Enrollments', fontsize=12, color='#fbfbff')
ax2.set_title('Biometric Age Group Distribution', fontsize=14, fontweight='bold', color='#fbfbff', pad=20)

for i, (val, pct) in enumerate(zip(age_group_values, age_group_pcts)):
    ax2.text(i, pct + 1, f"{pct:.1f}%\n({val/1000000:.1f}M)", 
             ha='center', fontsize=10, color='#fbfbff')

plt.tight_layout()
plt.savefig('biometric_analysis.png', dpi=100, facecolor='#1D1D20', edgecolor='none', bbox_inches='tight')
print("\n✅ Visualization saved: biometric_analysis.png")

print("\n" + "=" * 80)
print("✅ BIOMETRIC MODALITY ANALYSIS COMPLETE")
print("=" * 80)