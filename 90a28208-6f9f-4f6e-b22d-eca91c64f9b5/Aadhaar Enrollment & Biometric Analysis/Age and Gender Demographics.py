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
print("👥 AGE GROUP DEMOGRAPHICS ANALYSIS")
print("=" * 80)

# 1. ENROLLMENT DATA AGE DISTRIBUTION
print("\n📊 ENROLLMENT DATA - AGE GROUP DISTRIBUTION")
print("-" * 80)

enroll_df = integrated_dataset[integrated_dataset[['age_0_5', 'age_5_17', 'age_18_greater']].notna().all(axis=1)].copy()

total_age_0_5 = enroll_df['age_0_5'].sum()
total_age_5_17 = enroll_df['age_5_17'].sum()
total_age_18_plus = enroll_df['age_18_greater'].sum()
total_enrollment = total_age_0_5 + total_age_5_17 + total_age_18_plus

print(f"\nAge 0-5: {total_age_0_5:,.0f} ({total_age_0_5/total_enrollment*100:.2f}%)")
print(f"Age 5-17: {total_age_5_17:,.0f} ({total_age_5_17/total_enrollment*100:.2f}%)")
print(f"Age 18+: {total_age_18_plus:,.0f} ({total_age_18_plus/total_enrollment*100:.2f}%)")
print(f"Total Enrollments: {total_enrollment:,.0f}")

# 2. DEMOGRAPHIC DATA AGE DISTRIBUTION
print("\n\n📊 DEMOGRAPHIC DATA - AGE GROUP DISTRIBUTION")
print("-" * 80)

demo_df = integrated_dataset[integrated_dataset[['demo_age_5_17', 'demo_age_17_']].notna().all(axis=1)].copy()

total_demo_5_17 = demo_df['demo_age_5_17'].sum()
total_demo_17_plus = demo_df['demo_age_17_'].sum()
total_demo = total_demo_5_17 + total_demo_17_plus

print(f"\nAge 5-17: {total_demo_5_17:,.0f} ({total_demo_5_17/total_demo*100:.2f}%)")
print(f"Age 17+: {total_demo_17_plus:,.0f} ({total_demo_17_plus/total_demo*100:.2f}%)")
print(f"Total Demographic Records: {total_demo:,.0f}")

# 3. BIOMETRIC DATA AGE DISTRIBUTION
print("\n\n📊 BIOMETRIC DATA - AGE GROUP DISTRIBUTION")
print("-" * 80)

bio_df = integrated_dataset[integrated_dataset[['bio_age_5_17', 'bio_age_17_']].notna().all(axis=1)].copy()

total_bio_5_17 = bio_df['bio_age_5_17'].sum()
total_bio_17_plus = bio_df['bio_age_17_'].sum()
total_bio = total_bio_5_17 + total_bio_17_plus

print(f"\nAge 5-17: {total_bio_5_17:,.0f} ({total_bio_5_17/total_bio*100:.2f}%)")
print(f"Age 17+: {total_bio_17_plus:,.0f} ({total_bio_17_plus/total_bio*100:.2f}%)")
print(f"Total Biometric Records: {total_bio:,.0f}")

# 4. AGE DISTRIBUTION BY STATE (TOP 10 STATES)
print("\n\n📍 AGE DISTRIBUTION BY TOP 10 STATES (Enrollment Data)")
print("-" * 80)

state_age_summary = enroll_df.groupby('state').agg({
    'age_0_5': 'sum',
    'age_5_17': 'sum',
    'age_18_greater': 'sum'
})
state_age_summary['total'] = state_age_summary.sum(axis=1)
state_age_summary = state_age_summary.sort_values('total', ascending=False).head(10)

state_age_summary['pct_0_5'] = (state_age_summary['age_0_5'] / state_age_summary['total'] * 100).round(2)
state_age_summary['pct_5_17'] = (state_age_summary['age_5_17'] / state_age_summary['total'] * 100).round(2)
state_age_summary['pct_18_plus'] = (state_age_summary['age_18_greater'] / state_age_summary['total'] * 100).round(2)

print(state_age_summary[['total', 'pct_0_5', 'pct_5_17', 'pct_18_plus']].to_string())

# 5. GENDER DISTRIBUTION ANALYSIS
print("\n\n⚠️  GENDER DISTRIBUTION ANALYSIS")
print("-" * 80)
print("NOTE: Gender-specific data is not available in the current datasets.")
print("The available datasets contain only age group breakdowns without gender information.")
print("To perform gender distribution analysis, additional data sources would be required.")

# Create comprehensive age distribution visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Chart 1: Overall Age Distribution Comparison
datasets = ['Enrollment', 'Demographic', 'Biometric']
age_groups = ['0-5', '5-17', '17+']

# Prepare data for enrollment
enroll_pcts = [
    total_age_0_5/total_enrollment*100,
    total_age_5_17/total_enrollment*100,
    total_age_18_plus/total_enrollment*100
]

# For demographic (no 0-5 group)
demo_pcts = [0, total_demo_5_17/total_demo*100, total_demo_17_plus/total_demo*100]

# For biometric (no 0-5 group)
bio_pcts = [0, total_bio_5_17/total_bio*100, total_bio_17_plus/total_bio*100]

x = np.arange(len(age_groups))
width = 0.25

bars1 = ax1.bar(x - width, enroll_pcts, width, label='Enrollment', color=zerve_colors[0])
bars2 = ax1.bar(x, demo_pcts, width, label='Demographic', color=zerve_colors[1])
bars3 = ax1.bar(x + width, bio_pcts, width, label='Biometric', color=zerve_colors[2])

ax1.set_xlabel('Age Groups', fontsize=12, color='#fbfbff')
ax1.set_ylabel('Percentage (%)', fontsize=12, color='#fbfbff')
ax1.set_title('Age Group Distribution by Data Source', fontsize=14, fontweight='bold', color='#fbfbff', pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(age_groups)
ax1.legend(loc='upper right', framealpha=0.9)

# Add value labels
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}%', ha='center', va='bottom', fontsize=9, color='#fbfbff')

# Chart 2: Age Distribution in Top 10 States (Stacked)
states = state_age_summary.index[:10]
pct_0_5_vals = state_age_summary['pct_0_5'].values[:10]
pct_5_17_vals = state_age_summary['pct_5_17'].values[:10]
pct_18_plus_vals = state_age_summary['pct_18_plus'].values[:10]

x_pos = np.arange(len(states))
p1 = ax2.bar(x_pos, pct_0_5_vals, color=zerve_colors[0], label='Age 0-5')
p2 = ax2.bar(x_pos, pct_5_17_vals, bottom=pct_0_5_vals, color=zerve_colors[1], label='Age 5-17')
p3 = ax2.bar(x_pos, pct_18_plus_vals, bottom=pct_0_5_vals+pct_5_17_vals, color=zerve_colors[2], label='Age 18+')

ax2.set_ylabel('Percentage (%)', fontsize=12, color='#fbfbff')
ax2.set_title('Age Distribution in Top 10 States (Enrollment)', fontsize=14, fontweight='bold', color='#fbfbff', pad=20)
ax2.set_xticks(x_pos)
ax2.set_xticklabels(states, rotation=45, ha='right', fontsize=9)
ax2.legend(loc='upper right', framealpha=0.9)

plt.tight_layout()
plt.savefig('age_distribution_analysis.png', dpi=100, facecolor='#1D1D20', edgecolor='none', bbox_inches='tight')
print("\n✅ Visualization saved: age_distribution_analysis.png")

print("\n" + "=" * 80)
print("✅ DEMOGRAPHIC ANALYSIS COMPLETE")
print("=" * 80)