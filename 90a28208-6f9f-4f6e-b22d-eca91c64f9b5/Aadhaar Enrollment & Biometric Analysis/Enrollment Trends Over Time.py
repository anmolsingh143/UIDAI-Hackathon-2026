import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

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
print("📈 ENROLLMENT TRENDS OVER TIME")
print("=" * 80)

# Parse dates and create temporal analysis
trend_df = integrated_dataset.copy()
trend_df['date_parsed'] = pd.to_datetime(trend_df['date'], format='%d-%m-%Y', errors='coerce')

# Remove rows with invalid dates
trend_df = trend_df[trend_df['date_parsed'].notna()]

# Group by date for overall trends
daily_trends = trend_df.groupby('date_parsed').agg({
    'age_0_5': 'sum',
    'age_5_17': 'sum',
    'age_18_greater': 'sum',
    'demo_age_5_17': 'sum',
    'demo_age_17_': 'sum',
    'bio_age_5_17': 'sum',
    'bio_age_17_': 'sum'
}).fillna(0).sort_index()

print(f"\n📅 Date Range: {daily_trends.index.min().strftime('%Y-%m-%d')} to {daily_trends.index.max().strftime('%Y-%m-%d')}")
print(f"Total days with data: {len(daily_trends)}")

# Create temporal visualizations
trends_fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 14))

# Chart 1: Overall Enrollment Trend by Age Group
daily_trends['total_enrollment'] = daily_trends['age_0_5'] + daily_trends['age_5_17'] + daily_trends['age_18_greater']

ax1.plot(daily_trends.index, daily_trends['age_0_5']/1000, 
         label='Age 0-5', color=zerve_colors[0], linewidth=2)
ax1.plot(daily_trends.index, daily_trends['age_5_17']/1000, 
         label='Age 5-17', color=zerve_colors[1], linewidth=2)
ax1.plot(daily_trends.index, daily_trends['age_18_greater']/1000, 
         label='Age 18+', color=zerve_colors[2], linewidth=2)

ax1.set_xlabel('Date', fontsize=12, color='#fbfbff')
ax1.set_ylabel('Daily Enrollments (Thousands)', fontsize=12, color='#fbfbff')
ax1.set_title('Daily Enrollment Trends by Age Group', fontsize=14, fontweight='bold', color='#fbfbff', pad=20)
ax1.legend(loc='upper left', framealpha=0.9)
ax1.tick_params(axis='x', rotation=45)

# Chart 2: Total Enrollment Trend
ax2.plot(daily_trends.index, daily_trends['total_enrollment']/1000, 
         color=zerve_colors[4], linewidth=2.5)
ax2.fill_between(daily_trends.index, 0, daily_trends['total_enrollment']/1000, 
                 alpha=0.3, color=zerve_colors[4])

ax2.set_xlabel('Date', fontsize=12, color='#fbfbff')
ax2.set_ylabel('Total Daily Enrollments (Thousands)', fontsize=12, color='#fbfbff')
ax2.set_title('Overall Enrollment Trend', fontsize=14, fontweight='bold', color='#fbfbff', pad=20)
ax2.tick_params(axis='x', rotation=45)

# Chart 3: Demographic Data Trends
daily_trends['total_demo'] = daily_trends['demo_age_5_17'] + daily_trends['demo_age_17_']

ax3.plot(daily_trends.index, daily_trends['demo_age_5_17']/1000, 
         label='Demo Age 5-17', color=zerve_colors[1], linewidth=2)
ax3.plot(daily_trends.index, daily_trends['demo_age_17_']/1000, 
         label='Demo Age 17+', color=zerve_colors[3], linewidth=2)

ax3.set_xlabel('Date', fontsize=12, color='#fbfbff')
ax3.set_ylabel('Daily Demographic Records (Thousands)', fontsize=12, color='#fbfbff')
ax3.set_title('Demographic Data Collection Trends', fontsize=14, fontweight='bold', color='#fbfbff', pad=20)
ax3.legend(loc='upper left', framealpha=0.9)
ax3.tick_params(axis='x', rotation=45)

# Chart 4: Biometric Data Trends
daily_trends['total_bio'] = daily_trends['bio_age_5_17'] + daily_trends['bio_age_17_']

ax4.plot(daily_trends.index, daily_trends['bio_age_5_17']/1000, 
         label='Bio Age 5-17', color=zerve_colors[5], linewidth=2)
ax4.plot(daily_trends.index, daily_trends['bio_age_17_']/1000, 
         label='Bio Age 17+', color=zerve_colors[6], linewidth=2)

ax4.set_xlabel('Date', fontsize=12, color='#fbfbff')
ax4.set_ylabel('Daily Biometric Records (Thousands)', fontsize=12, color='#fbfbff')
ax4.set_title('Biometric Data Collection Trends', fontsize=14, fontweight='bold', color='#fbfbff', pad=20)
ax4.legend(loc='upper left', framealpha=0.9)
ax4.tick_params(axis='x', rotation=45)

plt.tight_layout()
trends_fig.savefig('enrollment_trends_over_time.png', dpi=100, facecolor='#1D1D20', edgecolor='none', bbox_inches='tight')
print(f"\n✅ Enrollment trends visualization saved: enrollment_trends_over_time.png")

# Print key statistics
print(f"\n📊 KEY TREND INSIGHTS:")
print(f"  • Peak daily enrollment: {daily_trends['total_enrollment'].max():,.0f}")
print(f"  • Average daily enrollment: {daily_trends['total_enrollment'].mean():,.0f}")
print(f"  • Peak demographic records: {daily_trends['total_demo'].max():,.0f}")
print(f"  • Peak biometric records: {daily_trends['total_bio'].max():,.0f}")

print("\n" + "=" * 80)