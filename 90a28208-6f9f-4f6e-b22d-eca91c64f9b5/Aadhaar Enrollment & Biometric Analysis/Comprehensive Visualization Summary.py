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
print("📊 COMPREHENSIVE ENROLLMENT VISUALIZATIONS - SUMMARY")
print("=" * 80)

# Create final summary dashboard combining key metrics
summary_fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 14))

# Chart 1: Overall Enrollment Distribution by Age Groups
age_group_names = ['Age 0-5', 'Age 5-17', 'Age 18+']
enrollment_totals = [
    integrated_dataset['age_0_5'].sum(),
    integrated_dataset['age_5_17'].sum(),
    integrated_dataset['age_18_greater'].sum()
]

# Filter out zero values for pie chart
nonzero_groups = [(name, val) for name, val in zip(age_group_names, enrollment_totals) if val > 0]
if nonzero_groups:
    names, values = zip(*nonzero_groups)
    colors_subset = [zerve_colors[i] for i in range(len(values))]
    
    wedges, texts, autotexts = ax1.pie(values, labels=names, autopct='%1.1f%%',
                                        colors=colors_subset, startangle=90,
                                        textprops={'color': '#fbfbff', 'fontsize': 11})
    for autotext in autotexts:
        autotext.set_color('#1D1D20')
        autotext.set_fontweight('bold')
    
    ax1.set_title('Overall Enrollment Distribution by Age Group', 
                  fontsize=14, fontweight='bold', color='#fbfbff', pad=20)

# Chart 2: Data Source Comparison
data_sources = ['Enrollment', 'Demographic', 'Biometric']
total_enroll = integrated_dataset[['age_0_5', 'age_5_17', 'age_18_greater']].sum().sum()
total_demo = integrated_dataset[['demo_age_5_17', 'demo_age_17_']].sum().sum()
total_bio = integrated_dataset[['bio_age_5_17', 'bio_age_17_']].sum().sum()

source_totals = [total_enroll/1e6, total_demo/1e6, total_bio/1e6]  # In millions

bars2 = ax2.bar(data_sources, source_totals, color=[zerve_colors[0], zerve_colors[1], zerve_colors[2]])
ax2.set_ylabel('Total Records (Millions)', fontsize=12, color='#fbfbff')
ax2.set_title('Total Records by Data Source', fontsize=14, fontweight='bold', color='#fbfbff', pad=20)

for _bar in bars2:
    _height = _bar.get_height()
    ax2.text(_bar.get_x() + _bar.get_width()/2., _height + 0.5,
            f'{_height:.1f}M', ha='center', va='bottom', fontsize=11, color='#fbfbff')

# Chart 3: Top 15 States by Total Enrollment
state_totals = integrated_dataset.groupby('state')[['age_0_5', 'age_5_17', 'age_18_greater']].sum()
state_totals['total'] = state_totals.sum(axis=1)
top_15_states_summary = state_totals.nlargest(15, 'total')

_y_pos = np.arange(len(top_15_states_summary))
bars3 = ax3.barh(_y_pos, top_15_states_summary['total']/1000, color=zerve_colors[4])
ax3.set_yticks(_y_pos)
ax3.set_yticklabels([s[:25] for s in top_15_states_summary.index], fontsize=9)
ax3.set_xlabel('Total Enrollment (Thousands)', fontsize=12, color='#fbfbff')
ax3.set_title('Top 15 States by Enrollment', fontsize=14, fontweight='bold', color='#fbfbff', pad=20)
ax3.invert_yaxis()

for _i, _val in enumerate(top_15_states_summary['total']/1000):
    ax3.text(_val + 10, _i, f'{_val:.0f}K', va='center', fontsize=9, color='#fbfbff')

# Chart 4: Biometric Capture Rate Analysis
bio_complete_records = integrated_dataset[integrated_dataset[['bio_age_5_17', 'bio_age_17_']].notna().all(axis=1)]
bio_by_state = bio_complete_records.groupby('state')[['bio_age_5_17', 'bio_age_17_']].sum()
bio_by_state['total_bio'] = bio_by_state.sum(axis=1)
top_12_bio_states = bio_by_state.nlargest(12, 'total_bio')

_y_pos_bio = np.arange(len(top_12_bio_states))
bars4 = ax4.barh(_y_pos_bio, top_12_bio_states['total_bio']/1000, color=zerve_colors[5])
ax4.set_yticks(_y_pos_bio)
ax4.set_yticklabels([s[:25] for s in top_12_bio_states.index], fontsize=9)
ax4.set_xlabel('Total Biometric Records (Thousands)', fontsize=12, color='#fbfbff')
ax4.set_title('Top 12 States by Biometric Capture', fontsize=14, fontweight='bold', color='#fbfbff', pad=20)
ax4.invert_yaxis()

for _i, _val in enumerate(top_12_bio_states['total_bio']/1000):
    ax4.text(_val + 50, _i, f'{_val:.0f}K', va='center', fontsize=9, color='#fbfbff')

plt.tight_layout()
summary_fig.savefig('comprehensive_enrollment_summary.png', dpi=100, facecolor='#1D1D20', edgecolor='none', bbox_inches='tight')
print("\n✅ Comprehensive summary visualization saved: comprehensive_enrollment_summary.png")

# Print final summary
print("\n" + "=" * 80)
print("📈 VISUALIZATION SUITE COMPLETE - KEY INSIGHTS")
print("=" * 80)

print(f"\n✅ Generated Visualizations:")
print(f"  1. Age Distribution Analysis (age_distribution_analysis.png)")
print(f"  2. Regional Enrollment Heatmaps (regional_enrollment_heatmaps.png)")
print(f"  3. Data Quality Dashboard (data_quality_dashboard.png)")
print(f"  4. Enrollment Trends Over Time (enrollment_trends_over_time.png)")
print(f"  5. Biometric Analysis (biometric_analysis.png)")
print(f"  6. Regional Analysis Charts (top_states_enrollment.png, enrollment_rate_distribution.png)")
print(f"  7. Comprehensive Summary (comprehensive_enrollment_summary.png)")

print(f"\n📊 Key Metrics Summary:")
print(f"  • Total unique states: {integrated_dataset['state'].nunique()}")
print(f"  • Total unique districts: {integrated_dataset['district'].nunique()}")
print(f"  • Total enrollment records: {total_enroll:,.0f}")
print(f"  • Total demographic records: {total_demo:,.0f}")
print(f"  • Total biometric records: {total_bio:,.0f}")
print(f"  • Date range covered: {integrated_dataset['date'].min()} to {integrated_dataset['date'].max()}")

print("\n" + "=" * 80)