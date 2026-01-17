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
print("📊 DATA QUALITY DASHBOARD")
print("=" * 80)

# Create comprehensive data quality visualization
quality_fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 14))

# Chart 1: Missing Data by Column
missing_cols = missing_analysis['Column'].tolist()
missing_pcts = missing_analysis['Missing %'].tolist()

bars = ax1.barh(missing_cols, missing_pcts, color=zerve_colors[3])
ax1.set_xlabel('Missing Data (%)', fontsize=12, color='#fbfbff')
ax1.set_title('Missing Data by Column', fontsize=14, fontweight='bold', color='#fbfbff', pad=20)
ax1.invert_yaxis()

for _i, (_col, _pct) in enumerate(zip(missing_cols, missing_pcts)):
    ax1.text(_pct + 1, _i, f'{_pct:.1f}%', va='center', fontsize=10, color='#fbfbff')

# Chart 2: Data Completeness by Source
sources = ['Enrollment\n(3 age groups)', 'Demographic\n(2 age groups)', 'Biometric\n(2 age groups)']
complete_counts = [enroll_complete, demo_complete, bio_complete]
total_records = len(integrated_dataset)
complete_pcts = [(count/total_records*100) for count in complete_counts]

bars2 = ax2.bar(sources, complete_pcts, color=[zerve_colors[0], zerve_colors[1], zerve_colors[2]])
ax2.set_ylabel('Completeness (%)', fontsize=12, color='#fbfbff')
ax2.set_title('Data Completeness by Source', fontsize=14, fontweight='bold', color='#fbfbff', pad=20)
ax2.set_ylim(0, 100)

for _bar in bars2:
    _height = _bar.get_height()
    ax2.text(_bar.get_x() + _bar.get_width()/2., _height + 2,
            f'{_height:.1f}%\n({int(_height * total_records / 100):,} rows)',
            ha='center', va='bottom', fontsize=10, color='#fbfbff')

# Chart 3: Duplicate Records Distribution
duplicate_summary = integrated_dataset.groupby('state').apply(
    lambda x: x.duplicated(subset=['date', 'state', 'district', 'pincode'], keep=False).sum()
).sort_values(ascending=False).head(15)

ax3.barh(range(len(duplicate_summary)), duplicate_summary.values, color=zerve_colors[4])
ax3.set_yticks(range(len(duplicate_summary)))
ax3.set_yticklabels(duplicate_summary.index, fontsize=9)
ax3.set_xlabel('Number of Duplicate Records', fontsize=12, color='#fbfbff')
ax3.set_title('Top 15 States by Duplicate Records', fontsize=14, fontweight='bold', color='#fbfbff', pad=20)
ax3.invert_yaxis()

for _i, _val in enumerate(duplicate_summary.values):
    ax3.text(_val + 100, _i, f'{_val:,}', va='center', fontsize=9, color='#fbfbff')

# Chart 4: Data Quality Metrics Summary
quality_metrics = [
    'Complete Records',
    'Partial Records', 
    'Zero Enrollments',
    'Duplicate Entries'
]

complete_all = integrated_dataset[numeric_cols].notna().all(axis=1).sum()
partial_records = len(integrated_dataset) - complete_all
zero_enrollments = zero_enroll.sum()
total_duplicates = duplicates.sum()

metric_counts = [complete_all, partial_records, zero_enrollments, total_duplicates]
metric_pcts = [(count/total_records*100) for count in metric_counts]

_x_pos = np.arange(len(quality_metrics))
bars4 = ax4.bar(_x_pos, metric_pcts, color=[zerve_colors[2], zerve_colors[1], zerve_colors[3], zerve_colors[4]])
ax4.set_ylabel('Percentage of Total Records (%)', fontsize=12, color='#fbfbff')
ax4.set_title('Data Quality Metrics Summary', fontsize=14, fontweight='bold', color='#fbfbff', pad=20)
ax4.set_xticks(_x_pos)
ax4.set_xticklabels(quality_metrics, rotation=15, ha='right', fontsize=10)

for _bar in bars4:
    _height = _bar.get_height()
    ax4.text(_bar.get_x() + _bar.get_width()/2., _height + 1,
            f'{_height:.1f}%', ha='center', va='bottom', fontsize=10, color='#fbfbff')

plt.tight_layout()
quality_fig.savefig('data_quality_dashboard.png', dpi=100, facecolor='#1D1D20', edgecolor='none', bbox_inches='tight')
print("\n✅ Data Quality Dashboard saved: data_quality_dashboard.png")

# Print summary statistics
print(f"\n📈 KEY DATA QUALITY INSIGHTS:")
print(f"  • Overall missing data rate: {total_missing_pct:.2f}%")
print(f"  • Complete records (all fields): {complete_all:,} ({complete_all/total_records*100:.1f}%)")
print(f"  • Records with zero enrollments: {zero_enrollments:,} ({zero_enrollments/total_records*100:.1f}%)")
print(f"  • Duplicate geographic/temporal entries: {total_duplicates:,} ({total_duplicates/total_records*100:.1f}%)")

print("\n" + "=" * 80)