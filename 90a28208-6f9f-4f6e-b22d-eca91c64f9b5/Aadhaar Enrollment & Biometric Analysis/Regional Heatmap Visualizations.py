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
print("🗺️  REGIONAL ENROLLMENT HEATMAPS")
print("=" * 80)

# Prepare state-level aggregation
state_enroll_summary = integrated_dataset.groupby('state').agg({
    'age_0_5': 'sum',
    'age_5_17': 'sum', 
    'age_18_greater': 'sum'
}).fillna(0)

state_enroll_summary['total_enrollment'] = state_enroll_summary.sum(axis=1)
state_enroll_summary = state_enroll_summary.sort_values('total_enrollment', ascending=False)

# Get top states for focused analysis
top_20_states = state_enroll_summary.head(20)

print(f"\n📊 Top 20 States by Total Enrollment:")
for _state, _row in top_20_states.iterrows():
    print(f"  {_state}: {_row['total_enrollment']:,.0f} enrollments")

# Create heatmap-style visualizations
heatmap_fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10))

# Chart 1: State Enrollment Intensity (Top 25)
top_25_states = state_enroll_summary.head(25)
_state_names = [s[:20] for s in top_25_states.index]  # Truncate long names
enrollment_values = top_25_states['total_enrollment'].values / 1000  # In thousands

# Create color gradient based on enrollment intensity
colors = plt.cm.YlOrRd(np.linspace(0.3, 0.9, len(enrollment_values)))

bars1 = ax1.barh(_state_names, enrollment_values, color=colors)
ax1.set_xlabel('Total Enrollment (Thousands)', fontsize=12, color='#fbfbff')
ax1.set_title('Enrollment Intensity Heatmap - Top 25 States', fontsize=14, fontweight='bold', color='#fbfbff', pad=20)
ax1.invert_yaxis()

# Add value labels
for _i, (_val, _bar) in enumerate(zip(enrollment_values, bars1)):
    ax1.text(_val + 5, _i, f'{_val:.0f}K', va='center', fontsize=9, color='#fbfbff')

# Chart 2: Age Group Distribution Heatmap (Top 20 States)
top_20_for_heatmap = state_enroll_summary.head(20)
age_group_data = top_20_for_heatmap[['age_0_5', 'age_5_17', 'age_18_greater']].values / 1000  # In thousands

# Create matrix heatmap
im = ax2.imshow(age_group_data, cmap='YlOrRd', aspect='auto')
ax2.set_xticks([0, 1, 2])
ax2.set_xticklabels(['Age 0-5', 'Age 5-17', 'Age 18+'], fontsize=11)
ax2.set_yticks(range(len(top_20_for_heatmap)))
ax2.set_yticklabels([s[:20] for s in top_20_for_heatmap.index], fontsize=9)
ax2.set_title('Age Group Distribution Heatmap - Top 20 States', fontsize=14, fontweight='bold', color='#fbfbff', pad=20)

# Add colorbar
cbar = plt.colorbar(im, ax=ax2)
cbar.set_label('Enrollment (Thousands)', rotation=270, labelpad=20, color='#fbfbff')
cbar.ax.yaxis.set_tick_params(color='#fbfbff')
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#fbfbff')

# Add value annotations to heatmap
for _i in range(len(top_20_for_heatmap)):
    for _j in range(3):
        _text_val = age_group_data[_i, _j]
        _text_color = '#1D1D20' if _text_val > age_group_data.max() * 0.5 else '#fbfbff'
        ax2.text(_j, _i, f'{_text_val:.0f}', ha='center', va='center', 
                color=_text_color, fontsize=8, fontweight='bold')

plt.tight_layout()
heatmap_fig.savefig('regional_enrollment_heatmaps.png', dpi=100, facecolor='#1D1D20', edgecolor='none', bbox_inches='tight')
print(f"\n✅ Regional heatmaps saved: regional_enrollment_heatmaps.png")

print("\n" + "=" * 80)