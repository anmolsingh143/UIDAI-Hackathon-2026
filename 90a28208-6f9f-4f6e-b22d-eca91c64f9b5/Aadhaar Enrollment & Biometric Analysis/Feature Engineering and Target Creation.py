import pandas as pd
import numpy as np

print("🔧 FEATURE ENGINEERING FOR MODELING")
print("=" * 60)

# Create a working copy
modeling_df = integrated_dataset.copy()

print(f"\n📊 Starting with {len(modeling_df):,} rows and {len(modeling_df.columns)} columns\n")

# ===================================================================
# 1. TARGET VARIABLE: Enrollment Completion
# ===================================================================
print("🎯 Creating Target Variable: enrollment_complete")
print("-" * 60)

# Define enrollment completion: all three data types exist (enrollment, demographic, biometric)
modeling_df['has_enrollment'] = (
    modeling_df['age_0_5'].notna() | 
    modeling_df['age_5_17'].notna() | 
    modeling_df['age_18_greater'].notna()
).astype(int)

modeling_df['has_demographic'] = (
    modeling_df['demo_age_5_17'].notna() | 
    modeling_df['demo_age_17_'].notna()
).astype(int)

modeling_df['has_biometric'] = (
    modeling_df['bio_age_5_17'].notna() | 
    modeling_df['bio_age_17_'].notna()
).astype(int)

# Target: 1 if all three data types exist, 0 otherwise
modeling_df['enrollment_complete'] = (
    (modeling_df['has_enrollment'] == 1) & 
    (modeling_df['has_demographic'] == 1) & 
    (modeling_df['has_biometric'] == 1)
).astype(int)

print(f"Target variable distribution:")
print(f"  Complete (1): {modeling_df['enrollment_complete'].sum():,} ({modeling_df['enrollment_complete'].mean()*100:.2f}%)")
print(f"  Incomplete (0): {(modeling_df['enrollment_complete'] == 0).sum():,} ({(1-modeling_df['enrollment_complete'].mean())*100:.2f}%)")

# ===================================================================
# 2. TEMPORAL FEATURES
# ===================================================================
print("\n⏰ Engineering Temporal Features")
print("-" * 60)

modeling_df['date'] = pd.to_datetime(modeling_df['date'], format='%d-%m-%Y', errors='coerce')
modeling_df['day_of_week'] = modeling_df['date'].dt.dayofweek
modeling_df['day_of_month'] = modeling_df['date'].dt.day
modeling_df['week_of_year'] = modeling_df['date'].dt.isocalendar().week.astype(float)
modeling_df['is_weekend'] = (modeling_df['day_of_week'] >= 5).astype(int)
modeling_df['is_month_start'] = (modeling_df['day_of_month'] <= 5).astype(int)
modeling_df['is_month_end'] = (modeling_df['day_of_month'] >= 26).astype(int)

print(f"  ✓ Created 6 temporal features")
print(f"    - day_of_week, day_of_month, week_of_year")
print(f"    - is_weekend, is_month_start, is_month_end")

# ===================================================================
# 3. ENROLLMENT METRICS (fill missing with 0 for aggregation)
# ===================================================================
print("\n📈 Engineering Enrollment Metrics")
print("-" * 60)

# Fill missing enrollment values with 0
enroll_cols = ['age_0_5', 'age_5_17', 'age_18_greater', 'demo_age_5_17', 
               'demo_age_17_', 'bio_age_5_17', 'bio_age_17_']

for col in enroll_cols:
    modeling_df[col] = modeling_df[col].fillna(0)

# Total enrollments by category
modeling_df['total_enrollment'] = (
    modeling_df['age_0_5'] + 
    modeling_df['age_5_17'] + 
    modeling_df['age_18_greater']
)

modeling_df['total_demographic'] = (
    modeling_df['demo_age_5_17'] + 
    modeling_df['demo_age_17_']
)

modeling_df['total_biometric'] = (
    modeling_df['bio_age_5_17'] + 
    modeling_df['bio_age_17_']
)

modeling_df['total_all_enrollments'] = (
    modeling_df['total_enrollment'] + 
    modeling_df['total_demographic'] + 
    modeling_df['total_biometric']
)

print(f"  ✓ Created enrollment totals")
print(f"    - total_enrollment, total_demographic, total_biometric")
print(f"    - total_all_enrollments")

# ===================================================================
# 4. AGE GROUP INDICATORS AND PROPORTIONS
# ===================================================================
print("\n👥 Engineering Age Group Features")
print("-" * 60)

# Age group indicators (binary)
modeling_df['has_age_0_5'] = (modeling_df['age_0_5'] > 0).astype(int)
modeling_df['has_age_5_17_enroll'] = (modeling_df['age_5_17'] > 0).astype(int)
modeling_df['has_age_18_plus'] = (modeling_df['age_18_greater'] > 0).astype(int)

# Age group proportions
modeling_df['pct_age_0_5'] = np.where(
    modeling_df['total_enrollment'] > 0,
    modeling_df['age_0_5'] / modeling_df['total_enrollment'] * 100,
    0
)

modeling_df['pct_age_5_17'] = np.where(
    modeling_df['total_enrollment'] > 0,
    modeling_df['age_5_17'] / modeling_df['total_enrollment'] * 100,
    0
)

modeling_df['pct_age_18_plus'] = np.where(
    modeling_df['total_enrollment'] > 0,
    modeling_df['age_18_greater'] / modeling_df['total_enrollment'] * 100,
    0
)

# Number of age groups covered
modeling_df['num_age_groups_covered'] = (
    modeling_df['has_age_0_5'] + 
    modeling_df['has_age_5_17_enroll'] + 
    modeling_df['has_age_18_plus']
)

print(f"  ✓ Created age group indicators and proportions")
print(f"    - Binary indicators for each age group")
print(f"    - Percentage distribution across age groups")
print(f"    - Number of age groups covered")

# ===================================================================
# 5. BIOMETRIC COMPLETENESS
# ===================================================================
print("\n🔐 Engineering Biometric Completeness Features")
print("-" * 60)

modeling_df['bio_completeness_score'] = (
    modeling_df['has_biometric'] * 100
)

modeling_df['bio_to_demo_ratio'] = np.where(
    modeling_df['total_demographic'] > 0,
    modeling_df['total_biometric'] / modeling_df['total_demographic'],
    0
)

modeling_df['bio_to_enroll_ratio'] = np.where(
    modeling_df['total_enrollment'] > 0,
    modeling_df['total_biometric'] / modeling_df['total_enrollment'],
    0
)

print(f"  ✓ Created biometric completeness features")
print(f"    - bio_completeness_score, bio_to_demo_ratio, bio_to_enroll_ratio")

# ===================================================================
# 6. REGIONAL/STATE-LEVEL AGGREGATIONS
# ===================================================================
print("\n🗺️  Engineering Regional Features")
print("-" * 60)

# State-level enrollment rates
state_enrollment_rate = modeling_df.groupby('state')['enrollment_complete'].mean()
modeling_df['state_enrollment_rate'] = modeling_df['state'].map(state_enrollment_rate)

# State-level average enrollments
state_avg_total = modeling_df.groupby('state')['total_all_enrollments'].mean()
modeling_df['state_avg_enrollments'] = modeling_df['state'].map(state_avg_total)

# State-level record count (how many records per state)
state_record_counts = modeling_df.groupby('state').size()
modeling_df['state_record_count'] = modeling_df['state'].map(state_record_counts)

# District-level enrollment rates
district_enrollment_rate = modeling_df.groupby(['state', 'district'])['enrollment_complete'].mean()
modeling_df['district_enrollment_rate'] = modeling_df.apply(
    lambda row: district_enrollment_rate.get((row['state'], row['district']), 0), 
    axis=1
)

# Pincode-level completeness
pincode_completeness = modeling_df.groupby('pincode')['enrollment_complete'].mean()
modeling_df['pincode_enrollment_rate'] = modeling_df['pincode'].map(pincode_completeness)

print(f"  ✓ Created regional aggregation features")
print(f"    - state_enrollment_rate, state_avg_enrollments, state_record_count")
print(f"    - district_enrollment_rate, pincode_enrollment_rate")

# ===================================================================
# 7. DATA QUALITY INDICATORS
# ===================================================================
print("\n✅ Engineering Data Quality Features")
print("-" * 60)

modeling_df['data_types_present'] = (
    modeling_df['has_enrollment'] + 
    modeling_df['has_demographic'] + 
    modeling_df['has_biometric']
)

modeling_df['is_partial_enrollment'] = (
    (modeling_df['data_types_present'] > 0) & 
    (modeling_df['data_types_present'] < 3)
).astype(int)

modeling_df['has_zero_enrollments'] = (
    modeling_df['total_all_enrollments'] == 0
).astype(int)

print(f"  ✓ Created data quality indicators")
print(f"    - data_types_present, is_partial_enrollment, has_zero_enrollments")

# ===================================================================
# SUMMARY OF ENGINEERED FEATURES
# ===================================================================
print("\n" + "=" * 60)
print("📋 FEATURE ENGINEERING COMPLETE")
print("=" * 60)

new_feature_cols = [
    # Target
    'enrollment_complete',
    # Helper columns
    'has_enrollment', 'has_demographic', 'has_biometric',
    # Temporal
    'day_of_week', 'day_of_month', 'week_of_year', 'is_weekend', 
    'is_month_start', 'is_month_end',
    # Enrollment metrics
    'total_enrollment', 'total_demographic', 'total_biometric', 'total_all_enrollments',
    # Age groups
    'has_age_0_5', 'has_age_5_17_enroll', 'has_age_18_plus',
    'pct_age_0_5', 'pct_age_5_17', 'pct_age_18_plus', 'num_age_groups_covered',
    # Biometric
    'bio_completeness_score', 'bio_to_demo_ratio', 'bio_to_enroll_ratio',
    # Regional
    'state_enrollment_rate', 'state_avg_enrollments', 'state_record_count',
    'district_enrollment_rate', 'pincode_enrollment_rate',
    # Data quality
    'data_types_present', 'is_partial_enrollment', 'has_zero_enrollments'
]

print(f"\n✨ Total engineered features: {len(new_feature_cols)}")
print(f"   Dataset shape: {modeling_df.shape}")
print(f"\n   Feature categories:")
print(f"   - Target variable: 1")
print(f"   - Helper columns: 3")
print(f"   - Temporal features: 6")
print(f"   - Enrollment metrics: 4")
print(f"   - Age group features: 7")
print(f"   - Biometric features: 3")
print(f"   - Regional features: 5")
print(f"   - Data quality features: 3")

print(f"\n✅ Feature engineering successful!")
