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
print("🗺️  REGIONAL ENROLLMENT ANALYSIS")
print("=" * 80)

# Filter to enrollment data only
enroll_df = integrated_dataset[integrated_dataset[['age_0_5', 'age_5_17', 'age_18_greater']].notna().all(axis=1)].copy()

# Calculate total enrollment per record
enroll_df['total_enrollment'] = enroll_df['age_0_5'] + enroll_df['age_5_17'] + enroll_df['age_18_greater']

# Regional Analysis by State
print("\n📍 ENROLLMENT BY STATE")
print("-" * 80)
state_enrollment = enroll_df.groupby('state').agg({
    'total_enrollment': 'sum',
    'age_0_5': 'sum',
    'age_5_17': 'sum',
    'age_18_greater': 'sum',
    'pincode': 'count'
}).rename(columns={'pincode': 'record_count'})

state_enrollment['avg_enrollment_per_record'] = state_enrollment['total_enrollment'] / state_enrollment['record_count']
state_enrollment = state_enrollment.sort_values('total_enrollment', ascending=False)

print("\nTop 15 States by Total Enrollment:")
print(state_enrollment.head(15)[['total_enrollment', 'record_count', 'avg_enrollment_per_record']].to_string())

# Calculate enrollment rates (as percentage of total)
state_enrollment['enrollment_rate'] = (state_enrollment['total_enrollment'] / state_enrollment['total_enrollment'].sum() * 100).round(2)

print("\n\nTop 10 States by Enrollment Rate (% of National Total):")
top_states = state_enrollment.nlargest(10, 'enrollment_rate')
print(top_states[['total_enrollment', 'enrollment_rate']].to_string())

# District-level analysis
print("\n\n📍 ENROLLMENT BY DISTRICT")
print("-" * 80)
district_enrollment = enroll_df.groupby(['state', 'district']).agg({
    'total_enrollment': 'sum',
    'pincode': 'count'
}).rename(columns={'pincode': 'record_count'}).sort_values('total_enrollment', ascending=False)

print("\nTop 15 Districts by Total Enrollment:")
print(district_enrollment.head(15).to_string())

# Regional patterns
print("\n\n📊 REGIONAL ENROLLMENT PATTERNS")
print("-" * 80)

# Calculate age distribution by state
state_age_dist = enroll_df.groupby('state').agg({
    'age_0_5': 'sum',
    'age_5_17': 'sum',
    'age_18_greater': 'sum'
})

state_age_dist['total'] = state_age_dist.sum(axis=1)
state_age_dist['pct_0_5'] = (state_age_dist['age_0_5'] / state_age_dist['total'] * 100).round(2)
state_age_dist['pct_5_17'] = (state_age_dist['age_5_17'] / state_age_dist['total'] * 100).round(2)
state_age_dist['pct_18_plus'] = (state_age_dist['age_18_greater'] / state_age_dist['total'] * 100).round(2)

print("Age Distribution Patterns in Top 10 States:")
top_10_states = state_enrollment.head(10).index
print(state_age_dist.loc[top_10_states, ['pct_0_5', 'pct_5_17', 'pct_18_plus']].to_string())

# Create visualization: Top 15 States by Total Enrollment
fig1, ax1 = plt.subplots(figsize=(14, 8))
top_15_states = state_enrollment.head(15)
bars = ax1.barh(range(len(top_15_states)), top_15_states['total_enrollment']/1000, color=zerve_colors[0])
ax1.set_yticks(range(len(top_15_states)))
ax1.set_yticklabels(top_15_states.index, fontsize=10)
ax1.set_xlabel('Total Enrollment (thousands)', fontsize=12, color='#fbfbff')
ax1.set_title('Top 15 States by Total Enrollment', fontsize=14, fontweight='bold', color='#fbfbff', pad=20)
ax1.invert_yaxis()

# Add value labels
for i, (idx, row) in enumerate(top_15_states.iterrows()):
    ax1.text(row['total_enrollment']/1000 + 1, i, f"{row['total_enrollment']/1000:.1f}K", 
             va='center', fontsize=9, color='#fbfbff')

plt.tight_layout()
plt.savefig('top_states_enrollment.png', dpi=100, facecolor='#1D1D20', edgecolor='none', bbox_inches='tight')
print("\n✅ Visualization saved: top_states_enrollment.png")

# Create visualization: Enrollment Rate Distribution
fig2, ax2 = plt.subplots(figsize=(14, 8))
top_12_by_rate = state_enrollment.nlargest(12, 'enrollment_rate')
bars = ax2.bar(range(len(top_12_by_rate)), top_12_by_rate['enrollment_rate'], color=zerve_colors[1])
ax2.set_xticks(range(len(top_12_by_rate)))
ax2.set_xticklabels(top_12_by_rate.index, rotation=45, ha='right', fontsize=10)
ax2.set_ylabel('Enrollment Rate (% of National Total)', fontsize=12, color='#fbfbff')
ax2.set_title('Top 12 States by Enrollment Rate', fontsize=14, fontweight='bold', color='#fbfbff', pad=20)

# Add value labels
for i, (idx, row) in enumerate(top_12_by_rate.iterrows()):
    ax2.text(i, row['enrollment_rate'] + 0.2, f"{row['enrollment_rate']:.1f}%", 
             ha='center', fontsize=9, color='#fbfbff')

plt.tight_layout()
plt.savefig('enrollment_rate_distribution.png', dpi=100, facecolor='#1D1D20', edgecolor='none', bbox_inches='tight')
print("✅ Visualization saved: enrollment_rate_distribution.png")

print("\n" + "=" * 80)
print("✅ REGIONAL ANALYSIS COMPLETE")
print("=" * 80)